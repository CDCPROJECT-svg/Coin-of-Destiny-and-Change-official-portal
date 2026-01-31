import sqlite3
import shutil
import os
from datetime import datetime

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
FILENAME = "CODAC_MAIN_KEYS.txt"
DESTINATION = "/sdcard/Download/" + FILENAME

def export_keys():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      💾 SAVING KEYS TO PHONE STORAGE...")
    print("=========================================================")

    # Get System Accounts (Level 99)
    cur.execute("SELECT name, wallet_address, private_key FROM active_members WHERE is_system_account = 99")
    rows = cur.fetchall()

    if not rows:
        print("   ❌ No Main Wallets found.")
        return

    # Write to file
    with open(FILENAME, "w") as f:
        f.write("=========================================================\n")
        f.write(f"   🔐 CODAC OFFICIAL MAIN KEYS - {datetime.now()}\n")
        f.write("   ⚠️  TOP SECRET: DO NOT SHARE THIS FILE\n")
        f.write("=========================================================\n\n")
        
        for name, addr, pkey in rows:
            f.write(f"📂 ACCOUNT: {name}\n")
            f.write(f"📬 ADDRESS: {addr}\n")
            f.write(f"🔑 PRIV KEY: {pkey}\n")
            f.write("-" * 50 + "\n")
            
    conn.close()
    
    # Move to Downloads
    try:
        shutil.copy(FILENAME, DESTINATION)
        print(f"   ✅ SUCCESS! File saved to: Downloads/{FILENAME}")
        print("   👉 Go to your File Manager > Downloads to see it.")
    except PermissionError:
        print("   ❌ ERROR: Permission Denied.")
        print("   👉 Please type: termux-setup-storage (and click Allow)")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Delete the copy inside Termux for security
    if os.path.exists(FILENAME):
        os.remove(FILENAME)

if __name__ == "__main__":
    export_keys()
