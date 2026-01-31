import sqlite3
import shutil
import os
from datetime import datetime

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
FILENAME = "CODAC_MASTER_VAULT_513.txt"
DESTINATION = "/sdcard/Download/" + FILENAME

def export_all():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🌍 EXPORTING ALL 513 WALLET KEYS...")
    print("=========================================================")

    # Select ALL accounts (Main Wallets + Regular Portals)
    # Ordered by ID for easier reading
    try:
        cur.execute("SELECT user_id, name, wallet_address, private_key FROM active_members ORDER BY user_id ASC")
        rows = cur.fetchall()

        if not rows:
            print("   ❌ No accounts found in the database.")
            return

        print(f"   📊 Found {len(rows)} accounts. Writing to file...")

        with open(FILENAME, "w") as f:
            f.write("=========================================================\n")
            f.write(f"   👑 CODAC MASTER VAULT (ALL 513 ACCOUNTS)\n")
            f.write(f"   DATE: {datetime.now()}\n")
            f.write("   ⚠️  TOP SECRET: CONTAINS ALL PRIVATE KEYS\n")
            f.write("=========================================================\n\n")
            
            for uid, name, addr, pkey in rows:
                # Handle empty keys if any
                addr = addr if addr else "NOT_GENERATED"
                pkey = pkey if pkey else "NOT_GENERATED"

                f.write(f"🆔 ID:       {uid}\n")
                f.write(f"👤 NAME:     {name}\n")
                f.write(f"📬 ADDRESS:  {addr}\n")
                f.write(f"🔑 PRIV KEY: {pkey}\n")
                f.write("-" * 50 + "\n")
        
        conn.close()

        # Move to Downloads
        if os.path.exists(DESTINATION):
            os.remove(DESTINATION) # Remove old file if exists
            
        shutil.copy(FILENAME, DESTINATION)
        
        # Cleanup Termux copy
        os.remove(FILENAME)

        print(f"\n   ✅ SUCCESS! Exported {len(rows)} keys.")
        print(f"   📂 File saved to: Downloads/{FILENAME}")
        print("   👉 PLEASE SECURE THIS FILE IMMEDIATELY.")

    except Exception as e:
        print(f"\n   ❌ Error: {e}")

if __name__ == "__main__":
    export_all()
