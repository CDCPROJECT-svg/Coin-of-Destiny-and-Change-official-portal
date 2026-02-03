import sqlite3
import csv
import os

# CONFIGURATION
DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
COUNTRY_LIST = "/data/data/com.termux/files/home/codac-coin_portal/languages_countries.txt"
EXPORT_FILE = "/data/data/com.termux/files/home/storage/downloads/CODAC_OFFICIAL_204_DEPLOYMENT.csv"

def export_official():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🌍 OFFICIAL 204 COUNTRIES EXPORT (STRICT)")
    print("=========================================================")

    # 1. CHECK MASTER LIST
    if not os.path.exists(COUNTRY_LIST):
        print("❌ ERROR: languages_countries.txt not found!")
        return

    official_names = []
    with open(COUNTRY_LIST, "r") as f:
        # Clean up lines and ignore empty ones
        official_names = [line.strip() for line in f if line.strip()]

    print(f"   📋 Reading Master List: {len(official_names)} Countries found.")
    
    # 2. MATCH WITH DATABASE
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    matches = []
    missing = []
    
    print("   🔍 Matching with Database Keys...")
    
    for country in official_names:
        # Try Exact Match first
        cur.execute("SELECT user_id, name, wallet_address, private_key FROM active_members WHERE name = ? COLLATE NOCASE", (country,))
        row = cur.fetchone()
        
        if row:
            matches.append(row)
        else:
            # Try Partial Match (e.g. 'Pilipinas' vs 'Philippines')
            cur.execute("SELECT user_id, name, wallet_address, private_key FROM active_members WHERE name LIKE ? COLLATE NOCASE", (f"%{country}%",))
            row = cur.fetchone()
            if row:
                matches.append(row)
            else:
                missing.append(country)

    # 3. SAVE TO CSV
    if matches:
        with open(EXPORT_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            # Header Row
            writer.writerow(["ID", "COUNTRY_NAME", "WALLET_ADDRESS", "PRIVATE_KEY"])
            # Data Rows
            writer.writerows(matches)

        print("-" * 57)
        print(f"   ✅ EXPORT SUCCESSFUL!")
        print(f"   📊 Total Countries Exported: {len(matches)}")
        print(f"   📂 File Saved: CODAC_OFFICIAL_204_DEPLOYMENT.csv")
        print(f"   📍 Location: Downloads Folder")
    else:
        print("   ❌ No matches found. Check database or list.")

    if missing:
        print("-" * 57)
        print(f"   ⚠️  WARNING: {len(missing)} Countries not found in DB:")
        # Show first 5 missing as sample
        for m in missing[:5]:
            print(f"      - {m}")
    
    conn.close()
    print("=========================================================")

if __name__ == "__main__":
    export_official()
