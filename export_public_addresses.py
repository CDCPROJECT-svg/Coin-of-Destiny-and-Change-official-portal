import sqlite3
import shutil
import os
from datetime import datetime

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
FILENAME = "CODAC_PUBLIC_DIRECTORY.txt"
DESTINATION = "/sdcard/Download/" + FILENAME

def export_public():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      📢 EXPORTING PUBLIC ADDRESSES (SAFE TO SHARE)...")
    print("=========================================================")

    # Select ID, Name, and Wallet Address ONLY (No Private Keys)
    try:
        cur.execute("SELECT user_id, name, wallet_address FROM active_members ORDER BY user_id ASC")
        rows = cur.fetchall()

        if not rows:
            print("   ❌ No accounts found.")
            return

        with open(FILENAME, "w") as f:
            f.write("=========================================================\n")
            f.write(f"   📬 CODAC OFFICIAL PUBLIC WALLET DIRECTORY\n")
            f.write(f"   DATE: {datetime.now()}\n")
            f.write("   ✅ STATUS: SAFE TO SHARE / FOR DEPOSITS ONLY\n")
            f.write("=========================================================\n\n")
            f.write(f" {'PORTAL ID':<20} | {'WALLET ADDRESS':<45} | {'NAME'}\n")
            f.write("-" * 100 + "\n")
            
            for uid, name, addr in rows:
                addr = addr if addr else "PENDING_GENERATION"
                f.write(f" {uid:<20} | {addr:<45} | {name}\n")
        
        conn.close()

        # Move to Downloads
        if os.path.exists(DESTINATION):
            os.remove(DESTINATION)
            
        shutil.copy(FILENAME, DESTINATION)
        os.remove(FILENAME) # Clean termux

        print(f"   ✅ SUCCESS! Exported {len(rows)} Public Addresses.")
        print(f"   📂 File saved to: Downloads/{FILENAME}")
        print("   👉 This file contains NO Private Keys. Safe to distribute.")

    except Exception as e:
        print(f"\n   ❌ Error: {e}")

if __name__ == "__main__":
    export_public()
