import pandas as pd
import json

XLSL_FILE = "Aura_Full_Project.xlsx"  # Your exported XLSX
OUTPUT_JSON = "paperweb_live.json"

EXTENSIONS = ["xlmath", "xlcode", "xldata", "xlflow", "xlviz", "xlweb", "xlaudio", "xlai"]
FUNCTION_COLUMN = 0  # Column with function names
PURPOSE_COLUMN = 1   # Column with purpose / description
SIGNATURE_COLUMN = 2 # Column with signature/parameters
EXAMPLE_COLUMN = 3   # Column with example input/output
NOTES_COLUMN = 4     # Column with notes

# -----------------------------
# Read XLSX & build structure
# -----------------------------
xls = pd.ExcelFile(XLSL_FILE)
paperweb = {"extensions": {}}

for ext in EXTENSIONS:
    ext_sheets = [s for s in xls.sheet_names if ext in s.lower()]
    paperweb["extensions"][ext] = {}
    for sheet in ext_sheets:
        df = pd.read_excel(xls, sheet)
        sheet_dict = {}
        if not df.empty:
            for i, row in df.iterrows():
                func_name = str(row[FUNCTION_COLUMN]) if pd.notna(row[FUNCTION_COLUMN]) else None
                if func_name:
                    sheet_dict[func_name] = {
                        "purpose": str(row[PURPOSE_COLUMN]) if pd.notna(row[PURPOSE_COLUMN]) else "",
                        "signature": str(row[SIGNATURE_COLUMN]) if pd.notna(row[SIGNATURE_COLUMN]) else "",
                        "example": str(row[EXAMPLE_COLUMN]) if pd.notna(row[EXAMPLE_COLUMN]) else "",
                        "notes": str(row[NOTES_COLUMN]) if pd.notna(row[NOTES_COLUMN]) else ""
                    }
        paperweb["extensions"][ext][sheet] = sheet_dict

# Save JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(paperweb, f, indent=2)

print(f"✅ Fully populated JSON created: {OUTPUT_JSON}")
