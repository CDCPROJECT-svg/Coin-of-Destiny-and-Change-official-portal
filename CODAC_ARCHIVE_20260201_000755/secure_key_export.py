import sqlite3
import os
from datetime import datetime

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
SECRET_FILE = "/data/data/com.termux/files/home/codac-coin_portal/TOP_SECRET_KEYS.txt"

def extract_keys():
    # Security Warning
    print("\033[H\033[J", end="")
    print("=========================================================================")
    print("   ⚠️  WARNING: YOU ARE ABOUT TO EXPORT PRIVATE KEYS")
    print("   This file grants total control over all accounts.")
    print("=========================================================================")
    
    confirm = input("   Type 'AUTHORITY' to proceed: ").strip()
    
    if confirm != "AUTHORITY":
        print("   ❌ ACCESS DENIED.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Check if columns exist
    try:
        cur.execute("SELECT user_id, name, wallet_address, private_key FROM active_members")
        rows = cur.fetchall()
    except sqlite3.OperationalError:
        print("\n   ⚠️  DATABASE ALERT: 'private_key' column not found.")
        print("   System Standard: Keys are usually generated locally per user")
        print("   and not stored centrally to prevent mass hacking.")
        conn.close()
        return

    with open(SECRET_FILE, "w") as f:
        f.write("=========================================================================\n")
        f.write(f"   🔐 CODAC PRIVATE KEY VAULT - DO NOT SHARE - {datetime.now()}\n")
        f.write("=========================================================================\n\n")
        
        for row in rows:
            uid, name, address, pkey = row
            # Fallback if empty
            address = address if address else "NOT_GENERATED"
            pkey = pkey if pkey else "ENCRYPTED_OR_MISSING"
            
            f.write(f"PORTAL ID:      {uid}\n")
            f.write(f"ACCOUNT NAME:   {name}\n")
            f.write(f"WALLET ADDRESS: {address}\n")
            f.write(f"PRIVATE KEY:    {pkey}\n")
            f.write("-" * 70 + "\n")

    conn.close()
    print(f"\n   ✅ SUCCESS: Keys exported to {SECRET_FILE}")
    print("   👉 MOVE THIS FILE TO A SECURE OFFLINE STORAGE IMMEDIATELY.")

if __name__ == "__main__":
    extract_keys()
