import sqlite3
import os

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
EXPORT_FILE = "/sdcard/Download/CODAC_COMPLETE_531_DATABASE.txt"

def view_everything():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      📂 OPENING ALL 531 DATABASE RECORDS")
    print("=========================================================")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Walang filter, walang limit. Lahat ng 531 kukunin natin.
    cur.execute("SELECT user_id, name, wallet_address, private_key FROM active_members ORDER BY rowid ASC")
    rows = cur.fetchall()

    with open(EXPORT_FILE, "w") as f:
        f.write("================================================================\n")
        f.write(f"   CODAC MASTER DATABASE - FULL DUMP (531 RECORDS)\n")
        f.write("================================================================\n\n")
        
        for i, row in enumerate(rows, 1):
            uid, name, addr, key = row
            f.write(f"REC #{i:03d}\n")
            f.write(f"ID:     {uid}\n")
            f.write(f"NAME:   {name}\n")
            f.write(f"ADDR:   {addr}\n")
            f.write(f"KEY:    {key}\n")
            f.write("-" * 40 + "\n")

    print(f"   ✅ SUCCESS! All {len(rows)} records are now visible.")
    print(f"   📂 File: CODAC_COMPLETE_531_DATABASE.txt")
    print(f"   📍 Location: Downloads Folder")
    print("=========================================================")
    conn.close()

if __name__ == "__main__":
    view_everything()
