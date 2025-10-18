import os
import datetime

def apply_improvements(improvements):
    applied = []
    os.makedirs("brain/data/improvements", exist_ok=True)

    for i, imp in enumerate(improvements):
        patch_name = f"brain/data/improvements/{datetime.date.today()}_patch_{i+1}.py"
        with open(patch_name, "w") as f:
            f.write(imp["code"])
        applied.append(patch_name)
        print(f"✅ Applied improvement: {imp['module']} ({imp['confidence']*100}%)")

    return applied
