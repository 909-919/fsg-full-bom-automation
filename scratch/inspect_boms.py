import pandas as pd
import glob
import os

files = glob.glob("BOMs/*.xlsx")
for f in files:
    print(f"File: {os.path.basename(f)}")
    try:
        df = pd.read_excel(f)
        df.columns = [str(c).strip().lower() for c in df.columns]
        if "system" in df.columns:
            print("Unique Systems:", df["system"].dropna().unique())
        if "assembly" in df.columns:
            print("Unique Assemblies:", df["assembly"].dropna().unique()[:10])
    except Exception as e:
        print("Error:", e)
    print("-" * 40)
