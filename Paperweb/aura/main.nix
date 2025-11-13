from fastapi import FastAPI
from .paperweb_router import router as paperweb_router
from .xlsl_engine import process_xlsl

app = FastAPI(title="Aura XLSL Paperweb")

app.include_router(paperweb_router, prefix="/paperweb")

@app.get("/")
def root():
    return {"message": "Aura XLSL Paperweb is alive 🚀"}

@app.post("/compute")
async def compute(data: dict):
    return process_xlsl(data)
