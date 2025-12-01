import os
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
XLSL_FILE = "Aura_Full_Project.xlsx"  # Export your .xlsl as .xlsx first
OUTPUT_DIR = "paperweb"

EXTENSIONS = ["xlmath", "xlcode", "xldata", "xlflow", "xlviz", "xlweb", "xlaudio", "xlai"]
SYSTEM_PAGES = ["engines", "xlsl", "pipelines"]

# Adjust if function names are stored in a specific column
FUNCTION_COLUMN = 0  

# -----------------------------
# Helper Functions
# -----------------------------
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_md(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_sheet_md(sheet_name, functions):
    content = f"# SHEET: {sheet_name}\n\n"
    content += "## 🎯 Purpose\nDescribe what this sheet does.\n\n"
    content += "## 🔧 Functions\n"
    for func in functions:
        content += f"- [{func}](../functions/{func}.md)\n"
    content += "\n## 🧩 Dependencies\nLinks to other sheets or extensions.\n\n"
    content += "## 🧪 Examples\nInput → Output examples\n\n"
    content += "## ⚙️ Internal Notes\nFor dev/debug\n"
    return content

def generate_function_md(func_name, sheet_name, extension_name):
    content = f"# FUNCTION: {func_name}\n\n"
    content += f"## Namespace\n{extension_name}\n\n"
    content += f"## Defined in Sheet\n[{sheet_name}](../sheets/{sheet_name}.md)\n\n"
    content += "## Signature\nDefine parameters here\n\n"
    content += "## Behavior\nExplain what this function does\n\n"
    content += "## Examples\nExample calls and outputs\n\n"
    content += "## Notes\nAdditional notes\n"
    return content

# -----------------------------
# Scaffold Directories
# -----------------------------
ensure_dir(OUTPUT_DIR)
ensure_dir(os.path.join(OUTPUT_DIR, "extensions"))
ensure_dir(os.path.join(OUTPUT_DIR, "sheets"))
ensure_dir(os.path.join(OUTPUT_DIR, "functions"))
ensure_dir(os.path.join(OUTPUT_DIR, "system"))

# -----------------------------
# Read XLSX & Parse Sheets
# -----------------------------
xls = pd.ExcelFile(XLSL_FILE)

sheet_function_map = {}  # sheet_name -> list of functions
all_functions = set()    # unique function names

for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name)
    if not df.empty:
        functions = df.iloc[:, FUNCTION_COLUMN].dropna().astype(str).tolist()
    else:
        functions = []
    sheet_function_map[sheet_name] = functions
    all_functions.update(functions)

# -----------------------------
# Generate Sheet Pages
# -----------------------------
for sheet_name, functions in sheet_function_map.items():
    md_content = generate_sheet_md(sheet_name, functions)
    write_md(os.path.join(OUTPUT_DIR, "sheets", f"{sheet_name}.md"), md_content)

# -----------------------------
# Generate Function Pages
# -----------------------------
for func_name in all_functions:
    # Find which sheet defines it
    sheet_name = next((s for s, funcs in sheet_function_map.items() if func_name in funcs), "unknown_sheet")
    # Map sheet to extension by naming pattern (adjust if needed)
    extension_name = next((ext for ext in EXTENSIONS if ext in sheet_name.lower()), "general")
    md_content = generate_function_md(func_name, sheet_name, extension_name)
    write_md(os.path.join(OUTPUT_DIR, "functions", f"{func_name}.md"), md_content)

# -----------------------------
# Generate Extension Pages
# -----------------------------
for ext in EXTENSIONS:
    # List all sheets in this extension (by matching name)
    sheets_in_ext = [s for s in xls.sheet_names if ext in s.lower()]
    content = f"# EXTENSION: {ext}\n\n## Purpose\nDescribe {ext} functionality.\n\n"
    content += "## Sheets\n"
    for sheet in sheets_in_ext:
        content += f"- [{sheet}](../sheets/{sheet}.md)\n"
    content += "\n## Notes\nAdditional extension info.\n"
    write_md(os.path.join(OUTPUT_DIR, "extensions", f"{ext}.md"), content)

# -----------------------------
# Generate System Pages
# -----------------------------
for page in SYSTEM_PAGES:
    sys_content = f"# SYSTEM PAGE: {page}\n\nDescribe the {page} here.\n"
    write_md(os.path.join(OUTPUT_DIR, "system", f"{page}.md"), sys_content)

# -----------------------------
# Generate Home Page with Table of Contents
# -----------------------------
toc = "# AURA.PAPERWEB\n\nYour universal sheet → page → function web.\n\n## Table of Contents\n"
for ext in EXTENSIONS:
    toc += f"- [{ext}](extensions/{ext}.md)\n"
    sheets_in_ext = [s for s in xls.sheet_names if ext in s.lower()]
    for sheet in sheets_in_ext:
        toc += f"  - [{sheet}](sheets/{sheet}.md)\n"
        for func in sheet_function_map[sheet]:
            toc += f"    - [{func}](functions/{func}.md)\n"

write_md(os.path.join(OUTPUT_DIR, "index.md"), toc)

print(f"✨ Fully interconnected Aura.paperweb generated in '{OUTPUT_DIR}' folder!")
