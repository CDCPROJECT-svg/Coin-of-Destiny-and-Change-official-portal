import sqlite3
import csv
import os

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
EXPORT_FILE = "/sdcard/Download/CODAC_OFFICIAL_204_COUNTRIES_COMPLETE.csv"

def extract_204():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🌍 EXTRACTING EXACTLY 204 COUNTRIES")
    print("=========================================================")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Kukunin natin ang lahat ng valid members (Exclude System, Proj, Team)
    # At lilimitahan natin sa 204
    cur.execute("""
        SELECT user_id, name, wallet_address, private_key 
        FROM active_members 
        WHERE is_system_account != 99 
        AND user_id NOT LIKE 'PROJ%' 
        AND user_id NOT LIKE 'CYCLE%' 
        AND user_id NOT LIKE 'TEAM%' 
        AND user_id NOT LIKE 'DEPT%'
        AND user_id != 'FOUNDER-001'
        ORDER BY name ASC
        LIMIT 204
    """)
    rows = cur.fetchall()

    count = len(rows)
    print(f"   📊 Found in Database: {count} Accounts")

    if count < 204:
        print(f"   ⚠️  WARNING: Database only has {count}. Missing {204 - count} to reach 204.")
    else:
        print(f"   ✅ PERFECT! Found exactly {count} entries.")

    # Save to CSV
    with open(EXPORT_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "COUNTRY_NAME", "WALLET_ADDRESS", "PRIVATE_KEY"])
        writer.writerows(rows)

    print("-" * 57)
    print(f"   ✅ SUCCESS! Extracted to: CODAC_OFFICIAL_204_COUNTRIES_COMPLETE.csv")
    print(f"   📍 Check Downloads folder.")
    
    # Verification
    print("\n   🔎 SAMPLE CHECK:")
    if count > 0: print(f"      1. {rows[0][1]}") # First
    if count >= 204: print(f"      204. {rows[203][1]}") # Last

    conn.close()
    print("=========================================================")

if __name__ == "__main__":
    extract_204()
