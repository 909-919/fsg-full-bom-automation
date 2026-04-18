import pandas as pd
from pathlib import Path
p = None
for f in Path('BOMs').glob('BOM_PT_EFR18*.xlsx'):
    p = f
    break
if not p:
    print('No BOM file found matching pattern in BOMs/')
    raise SystemExit(1)
print('Found:', p)

df = pd.read_excel(p)
# normalize headers
cols = [str(c).strip().lower() for c in df.columns]
df.columns = cols
if 'system' not in df.columns or 'assembly' not in df.columns:
    print('ERROR: missing required columns. Found:', df.columns.tolist())
    raise SystemExit(1)

# normalize system
df['system_norm'] = df['system'].astype(str).str.strip().str.upper()
dt = df[df['system_norm'] == 'DT']
print('DT rows total:', len(dt))
unique = sorted({str(a).strip() for a in dt['assembly'].dropna()})
print('\nUnique assemblies (DT):')
for i,a in enumerate(unique, start=1):
    print(f'{i:3d}. {a}')

# show rows where 'upright', 'gearbox', or 'motor' appear in assembly or part
for keyword in ['upright','gearbox','motor']:
    print('\nRows with keyword:', keyword)
    mask = dt['assembly'].astype(str).str.lower().str.contains(keyword) | dt.get('part', dt['assembly']).astype(str).str.lower().str.contains(keyword)
    subset = dt[mask]
    if subset.empty:
        print('  none')
    else:
        for idx,row in subset.iterrows():
            print(f"  Row {idx+2}: assembly={row['assembly']!r}, part={row.get('part')!r}")
