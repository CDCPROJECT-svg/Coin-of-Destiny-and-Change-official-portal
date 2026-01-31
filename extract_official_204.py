import sqlite3
import csv
import os

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
EXPORT_FILE = "/sdcard/Download/CODAC_OFFICIAL_204_EXTRACT.csv"

def extract_now():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🌍 EXTRACTING OFFICIAL 204 COUNTRIES")
    print("=========================================================")

    if not os.path.exists(DB_PATH):
        print("❌ Error: Database file not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Kukunin ang lahat ng may format na CODAC-A09L
    # Ito ang siguradong listahan ng bansa mo
    cur.execute("""
        SELECT user_id, name, wallet_address, private_key 
        FROM active_members 
        WHERE user_id LIKE 'CODAC-A09L-%'
        ORDER BY name ASC
    """)
    rows = cur.fetchall()

    if not rows:
        print("   ⚠️  Walang nahanap na may 'CODAC-A09L' format.")
        print("       Baka kailangan nating i-check ang database dump ulit.")
    else:
        with open(EXPORT_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "COUNTRY_NAME", "WALLET_ADDRESS", "PRIVATE_KEY"])
            writer.writerows(rows)

        print(f"   📊 Found {len(rows)} Formatted Countries.")
        print(f"   ✅ SUCCESS! Extracted to CSV.")
        print(f"   📂 File: CODAC_OFFICIAL_204_EXTRACT.csv")
        print(f"   📍 Location: Downloads Folder")

    conn.close()
    print("=========================================================")

if __name__ == "__main__":
    extract_now()
