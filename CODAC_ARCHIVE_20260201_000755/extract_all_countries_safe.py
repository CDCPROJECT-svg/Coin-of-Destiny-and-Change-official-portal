import sqlite3
import csv
import os

# FILES
DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
EXPORT_FILE = "/sdcard/Download/CODAC_ALL_COUNTRIES_FINAL_EXTRACT.csv"
COUNTRY_LIST = "/data/data/com.termux/files/home/codac-coin_portal/languages_countries.txt"

def safe_extract():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🌍 SAFE EXTRACTION: ALL COUNTRIES")
    print("=========================================================")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Load the Official List (Para sure na Bansa lang)
    if os.path.exists(COUNTRY_LIST):
        with open(COUNTRY_LIST, "r") as f:
            target_names = [line.strip() for line in f if line.strip()]
    else:
        # Fallback kung wala ang list file, kukunin lahat ng non-system
        target_names = []
        cur.execute("SELECT name FROM active_members WHERE is_system_account != 99 AND user_id NOT LIKE 'PROJ%' ORDER BY name ASC")
        for row in cur.fetchall():
            target_names.append(row[0])

    print(f"   📋 Target List: {len(target_names)} Countries")
    print("   🔍 Extracting keys...")

    extracted_data = []
    
    # 2. Match Database
    for country in target_names:
        # Hanapin sa DB by Name
        cur.execute("SELECT user_id, name, wallet_address, private_key FROM active_members WHERE name = ?", (country,))
        row = cur.fetchone()
        
        if row:
            extracted_data.append(row)
        else:
            # Try fuzzy match if exact fails
            cur.execute("SELECT user_id, name, wallet_address, private_key FROM active_members WHERE name LIKE ?", (f"%{country}%",))
            row = cur.fetchone()
            if row:
                extracted_data.append(row)

    # 3. Save to CSV
    if extracted_data:
        with open(EXPORT_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "COUNTRY_NAME", "WALLET_ADDRESS", "PRIVATE_KEY"])
            writer.writerows(extracted_data)

        print("-" * 57)
        print(f"   ✅ SUCCESS! Extracted {len(extracted_data)} Countries.")
        print(f"   📂 File: CODAC_ALL_COUNTRIES_FINAL_EXTRACT.csv")
        print(f"   📍 Location: Downloads Folder")
        
        # Check specific samples
        sudan = next((r for r in extracted_data if "Sudan" in r[1]), None)
        france = next((r for r in extracted_data if "France" in r[1]), None)
        
        if sudan: print(f"   ✅ Verified: Sudan is present.")
        if france: print(f"   ✅ Verified: France is present.")
        
    else:
        print("   ❌ No data extracted. Please check database.")

    conn.close()
    print("=========================================================")

if __name__ == "__main__":
    safe_extract()
