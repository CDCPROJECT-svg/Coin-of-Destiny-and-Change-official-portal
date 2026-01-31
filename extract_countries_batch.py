import sqlite3
import csv
import os

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
EXPORT_FILE = "/sdcard/Download/CODAC_204_COUNTRIES_BATCH.csv"

def extract_countries():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🌍 EXTRACTING 204 COUNTRIES (CLEAN LIST)")
    print("=========================================================")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Kukunin natin lahat ng members na HINDI System Account (99) at HINDI Project/Team
    # Aayusin natin Alphabetical (A-Z) para madaling makita ang France at Sudan
    query = """
        SELECT user_id, name, wallet_address, private_key 
        FROM active_members 
        WHERE is_system_account != 99 
        AND user_id NOT LIKE 'PROJ%' 
        AND user_id NOT LIKE 'CYCLE%'
        AND user_id NOT LIKE 'TEAM%'
        AND user_id NOT LIKE 'DEPT%'
        AND user_id != 'FOUNDER-001'
        ORDER BY name ASC
    """
    
    cur.execute(query)
    rows = cur.fetchall()

    if rows:
        print(f"   📊 Found {len(rows)} Countries/Members.")
        
        # Check for specific countries requested
        has_sudan = any("Sudan" in r[1] for r in rows)
        has_france = any("France" in r[1] for r in rows)
        
        if has_sudan: print("   ✅ Sudan found in list.")
        if has_france: print("   ✅ France found in list.")

        with open(EXPORT_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "COUNTRY_NAME", "WALLET_ADDRESS", "PRIVATE_KEY"])
            writer.writerows(rows)
            
        print("-" * 57)
        print(f"   ✅ EXPORT SUCCESS: {EXPORT_FILE}")
        print("   (Check Downloads folder for the clean list)")
    else:
        print("   ❌ No country data found in database.")

    conn.close()

if __name__ == "__main__":
    extract_countries()
