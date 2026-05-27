# 🏎️ FSG CCBOM Automation

> Automate the tedious process of manually entering parts into the [Formula Student Germany](https://www.formulastudent.de/) Bill of Material (BOM) tool — so you can focus on building fast cars.
<div align="center">

  ![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
  ![Playwright](https://img.shields.io/badge/Playwright-browser%20automation-green?logo=playwright&logoColor=white)
  ![License](https://img.shields.io/badge/License-MIT-yellow)
</div>

![FSG_Tool_Automation_Test_Demo](https://github.com/user-attachments/assets/16332de3-8680-460f-a5cd-947594e50dfe)

## ✨ Features

| Feature | Description |
|---|---|
| **Bulk Upload** | Reads your BOM Excel and uploads every part automatically |
| **Duplicate Detection** | Scrapes the existing BOM table before uploading — running it twice is safe |
| **Smart Assembly Matching** | Maps common names like *"brake caliper"* → *Calipers* automatically |
| **Row Filtering** | Skips example rows, empty rows, 🟢 green (already done), and 🔴 red (do not upload) |
| **Test Mode** | Limits uploads to the first N parts so you can verify before going all-in |
| **Configurable** | `.env` file for credentials, team ID, system filter, and more |
| **Audit Log** | Every action is logged to `bom_log.txt` with timestamps |

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/Woonderpipe/fsg-bom-automation.git

cd fsg-bom-automation
```
Create a virtual environment and activate it:

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```
Then
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

> Note: `requirements.txt` installs the Playwright Python package. The browser runtime itself still needs a separate install step.

### 2. Configure

```bash
# macOS / Linux
cp .env.example .env

# Windows PowerShell
copy .env.example .env
```

Edit `.env` with your FSG credentials and team ID:

```env
# Make sure to at least set these, before running the script! 
FSG_USERNAME=your_username
FSG_PASSWORD=your_password
TEAM_ID=YOUR_TEAM_ID
TEST_MODE=true
DRY_RUN=true
# More info on each and more variables is in the .env file itself.
```

> **🔑 Finding your Team ID:** Open your BOM page on the FSG website. The URL looks like:
> `https://www.formulastudent.de/teams/fse/details/bom/tid/YOUR_TEAM_ID`
> Your `TEAM_ID` is the number at the end — `359` in this example.

### 3. Prepare Your Excel Files

Place your `.xlsx` BOM files in the `BOMs/` folder:

> [!TIP]
> For best results, use the provided `BOM_Example_EFRxx.xlsx` as a starting point. Make sure to follow the required column headers and formatting (or edit the script if your format is different).

```
project/
├── BOMs/
│   ├── BOM_BR_MyTeam.xlsx
│   ├── BOM_SU_MyTeam.xlsx
│   ├── BOM_Example_EFRxx.xlsx
│   └── ...
├── main.py
├── .env
└── ...
```

### 4. Run

```bash
python main.py
```

The script will:
1. Let you pick an Excel file
2. Show you which systems are in the file
3. Open a browser, log you in, and start uploading (or simulate if `DRY_RUN=true`)
4. Print a summary of what was uploaded, skipped, or failed

---

## 📋 Excel Format

Your Excel file should have these column headers (case-insensitive):

| Column | Required | Description |
|---|---|---|
| `system` | ✅ | System code: `AT`, `BR`, `DT`, `ET`, `FR`, `LV`, `MS`, `ST`, `SU`, `WT` |
| `assembly` | ✅ | Assembly name (e.g. `Brake Pads`, `Calipers`) |
| `part` | ✅ | Part name (free text) |
| `part_quantity` | ❌ | Quantity (number) |
| `make o. buy` | ❌ | `m` for make, `b` for buy |
| `part_comments` | ❌ | Comments (free text) |

---

## 🧭 FSG Systems Reference

| Code | Full Name |
|---|---|
| `AT` | Autonomous System |
| `BR` | Brake System |
| `DT` | Drivetrain |
| `ET` | Engine and Tractive System |
| `FR` | Chassis and Body |
| `LV` | Grounded Low Voltage System |
| `MS` | Miscellaneous Fit and Finish |
| `ST` | Steering System |
| `SU` | Suspension System |
| `WT` | Wheels, Wheel Bearings and Tires |

---

## 🎨 Row Colour Coding

The script reads the background colour of the first few cells in each row (up to the first 5 columns). It supports common hex formats and also recognizes close shades of green and red.

| Colour | Behaviour |
|---|---|
| 🟢 **Green-like** | Skipped — already uploaded |
| 🔴 **Red-like** | Skipped — do not upload |
| ⬜ **No colour** | Processed normally |

> Use a green-like fill to mark rows as already uploaded, or a red-like fill to exclude rows from processing.

---

## 🧠 Smart Assembly Matching

The FSG website has fixed assembly names. If your Excel uses a slightly different name, the script remaps it automatically:

| Excel Name | → FSG Dropdown |
|---|---|
| `brake caliper` | Calipers |
| `reservoir` / `reservoire` | Brake Master Cylinder |
| `fitting screw` / `bolts` | Fasteners |
| `brake disc` / `brake disk` | Brake Discs |
| `damper` | Dampers |
| `tire` / `tyre` | Tires |
| ... and many more | |

> You can add your own mappings by editing `BOMs/config.yaml`.

---

## 🔒 Duplicate Detection

Before uploading, the script reads existing parts from the FSG website BOM table and compares each candidate row to the scraped site data.

- The comparison is based primarily on normalized part names.
- If both Excel and site rows include assembly names, the match also checks normalized assembly names.
- If a duplicate is detected, the row is logged as `SKIP` and not uploaded.
- Running the script again will avoid re-uploading parts already present on the site.

---

## 🪵 Log Output

Every run appends to `bom_log.txt`:

```
[2026-04-08 21:11:02] [INFO] Found 358 existing parts on the website.
[2026-04-08 21:11:05] [OK]   Row 12: ✓ 'Caliper front'
[2026-04-08 21:11:07] [OK]   Row 13: ✓ 'Caliper rear'
[2026-04-08 21:11:10] [SKIP] Row 14: Duplicate — 'Washer M5' already exists
[2026-04-08 21:12:36] [ERROR] Row 38: ✗ 'tape' — Timeout 5000ms exceeded.
[2026-04-08 21:13:19] [INFO] Done in 137.2s — 35 uploaded / 3 duplicates / 1 failed
```

---

## 🛟 Troubleshooting

| Problem | Solution |
|---|---|
| **Login fails** | The browser will still open — log in manually, navigate to the BOM page, then press Enter |
| **"Assembly not found"** | Add a mapping to `BOMs/config.yaml` |
| **Timeout errors** | Can happen if the FSG server is slow. Re-run — duplicates are safe |
| **Column not found** | Ensure your Excel headers match: `system`, `assembly`, `part` |
| **No Excel files found** | Place `.xlsx` files in the `BOMs/` folder |
| **Other Issues or Bugs or Improvement Ideas** | Feel free to make a Pull Request or contact Sharbel from ELBFLORACE e.V. |

---

## 🔒 Security

If you discover a security issue, please open a GitHub issue or pull request. See `SECURITY.md` for details.

## 📄 License

MIT — use it, share it, improve it. Built with 🧡 by Sharbel from [ELBFLORACE e.V.](https://elbflorace.de/en)

---


> [!NOTE] 
> Note to FSG: If you're seeing this — please consider adding a CSV/bulk import feature to the CCBOM tool natively. Every team spends hours on manual data entry that could be automated. We built this tool out of necessity, but a first-party solution would be far better for the entire community. 🙏