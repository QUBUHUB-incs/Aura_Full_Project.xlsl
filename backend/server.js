# server.py
import os
import shutil
import sqlite3
import subprocess
import uuid
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiofiles
import httpx

# -------------------------
# Configuration (edit env or values)
# -------------------------
DATA_DIR = os.environ.get("AURA_DATA_DIR", "./aura_data")  # local workspace root
DB_PATH = os.environ.get("AURA_DB_PATH", "./aura_meta.db")
API_KEY = os.environ.get("AURA_API_KEY", "changeme")  # strong shared secret for local usage
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # optional, used by /api/llm proxy
RCLONE_REMOTE_NAME = os.environ.get("RCLONE_REMOTE", "icloud:")  # if using rclone (optional)

os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------
# Simple DB for sessions/logs
# -------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    ts TEXT,
                    name TEXT,
                    metadata TEXT,
                    filepath TEXT
                )""")
    conn.commit()
    conn.close()

init_db()

# -------------------------
# FastAPI app + CORS
# -------------------------
app = FastAPI(title="Aura Lab Bridge")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Helpers
# -------------------------
def check_api_key(x_api_key: str | None):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

def safe_path_join(base: str, path: str):
    # prevent path traversal
    target = os.path.normpath(os.path.join(base, path))
    if not target.startswith(os.path.abspath(base)):
        raise HTTPException(status_code=400, detail="Invalid path")
    return target

# -------------------------
# Pydantic models
# -------------------------
class UploadMeta(BaseModel):
    name: str | None = None
    metadata: dict | None = None
    path: str | None = None  # relative path inside DATA_DIR

class LLMRequest(BaseModel):
    prompt: str
    max_tokens: int | None = 300

# -------------------------
# Endpoints
# -------------------------

@app.get("/health")
async def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

# 1) List files in workspace
@app.get("/files/list")
async def list_files(path: str = "", x_api_key: str | None = Header(None)):
    check_api_key(x_api_key)
    target = safe_path_join(DATA_DIR, path)
    if not os.path.exists(target):
        raise HTTPException(404, "Path not found")
    entries = []
    for name in os.listdir(target):
        p = os.path.join(target, name)
        entries.append({
            "name": name,
            "is_dir": os.path.isdir(p),
            "size": os.path.getsize(p) if os.path.isfile(p) else None,
            "mtime": os.path.getmtime(p)
        })
    return {"path": path, "entries": entries}

# 2) Read file
@app.get("/files/read")
async def read_file(path: str, x_api_key: str | None = Header(None)):
    check_api_key(x_api_key)
    target = safe_path_join(DATA_DIR, path)
    if not os.path.isfile(target):
        raise HTTPException(404, "File not found")
    return FileResponse(target, filename=os.path.basename(target))

# 3) Upload (browser uploads file to server)
@app.post("/files/upload")
async def upload_file(
    meta: str | None = None,
    file: UploadFile | None = File(None),
    x_api_key: str | None = Header(None)
):
    check_api_key(x_api_key)
    if file is None:
        raise HTTPException(400, "No file uploaded")
    # optional relative path in meta (json) — but keep safe
    out_name = file.filename
    out_path = os.path.join(DATA_DIR, out_name)
    # avoid overwriting accidentally — add uuid
    out_path = safe_path_join(DATA_DIR, out_name)
    # write file async
    async with aiofiles.open(out_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    # persist a session row
    sid = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO sessions (id, ts, name, metadata, filepath) VALUES (?,?,?,?,?)",
                (sid, datetime.utcnow().isoformat(), file.filename, meta or "{}", os.path.relpath(out_path, DATA_DIR)))
    conn.commit(); conn.close()
    return {"ok": True, "path": os.path.relpath(out_path, DATA_DIR), "session_id": sid}

# 4) Download a file (mirror)
@app.get("/files/download")
async def download_file(path: str, x_api_key: str | None = Header(None)):
    check_api_key(x_api_key)
    target = safe_path_join(DATA_DIR, path)
    if not os.path.isfile(target):
        raise HTTPException(404, "File not found")
    return FileResponse(target, filename=os.path.basename(target))

# 5) Write plain text to file
@app.post("/files/write")
async def write_text(path: str, content: str, x_api_key: str | None = Header(None)):
    check_api_key(x_api_key)
    target = safe_path_join(DATA_DIR, path)
    # create dirs
    os.makedirs(os.path.dirname(target), exist_ok=True)
    async with aiofiles.open(target, 'w') as f:
        await f.write(content)
    return {"ok": True, "path": os.path.relpath(target, DATA_DIR)}

# 6) List sessions
@app.get("/sessions")
async def list_sessions(x_api_key: str | None = Header(None)):
    check_api_key(x_api_key)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, ts, name, metadata, filepath FROM sessions ORDER BY ts DESC LIMIT 200")
    rows = cur.fetchall()
    conn.close()
    sessions = [{"id": r[0], "ts": r[1], "name": r[2], "metadata": r[3], "filepath": r[4]} for r in rows]
    return {"sessions": sessions}

# 7) LLM proxy endpoint (server-side uses OPENAI_API_KEY or other provider)
@app.post("/api/llm")
async def llm_proxy(req: LLMRequest, x_api_key: str | None = Header(None)):
    check_api_key(x_api_key)
    if not OPENAI_API_KEY:
        raise HTTPException(500, "LLM backend not configured on server (OPENAI_API_KEY missing)")
    # Example call to OpenAI Chat Completions (replace URL/payload as your provider requires)
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": req.prompt}],
        "max_tokens": req.max_tokens or 300,
        "temperature": 0.6
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, json=payload, headers=headers)
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"LLM error: {resp.status_code} {resp.text[:200]}")
        data = resp.json()
        # simple normalization: try to extract first assistant text
        try:
            choice_text = data["choices"][0]["message"]["content"]
        except Exception:
            choice_text = str(data)
        return {"text": choice_text, "raw": data}

# 8) rclone-driven cloud sync helpers (optional)
# Requires 'rclone' installed and configured on server with a remote name in RCLONE_REMOTE_NAME
@app.post("/sync/push")
async def sync_push(path: str, remote_path: str = "", x_api_key: str | None = Header(None)):
    check_api_key(x_api_key)
    target = safe_path_join(DATA_DIR, path)
    if not os.path.exists(target):
        raise HTTPException(404, "Path not found")
    # call rclone copy
    remote_uri = f"{RCLONE_REMOTE_NAME.rstrip(':')}:{remote_path}".rstrip(':')
    cmd = ["rclone", "copy", target, remote_uri, "--progress"]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        return {"ok": True, "cmd": " ".join(cmd), "stdout": proc.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"rclone failed: {e.stderr[:400]}")

@app.post("/sync/pull")
async def sync_pull(remote_path: str, local_path: str = "", x_api_key: str | None = Header(None)):
    check_api_key(x_api_key)
    local_target = safe_path_join(DATA_DIR, local_path or "")
    os.makedirs(local_target, exist_ok=True)
    remote_uri = f"{RCLONE_REMOTE_NAME.rstrip(':')}:{remote_path}"
    cmd = ["rclone", "copy", remote_uri, local_target, "--progress"]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        return {"ok": True, "cmd": " ".join(cmd), "stdout": proc.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"rclone failed: {e.stderr[:400]}")

# -------------------------
# Run: uvicorn server:app --host 0.0.0.0 --port 8000
# -------------------------
