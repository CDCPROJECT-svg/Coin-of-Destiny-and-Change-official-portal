import sqlite3
import random

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def inspect():
    if not os.path.exists(DB_PATH):
        print("❌ Error: Database not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="") # Clear Screen
    print("=====================================================================")
    print("                  📂 CODAC MASTER DATABASE INSPECTOR")
    print("=====================================================================")

    # 1. STATISTICS
    cur.execute("SELECT count(*) FROM active_members")
    total = cur.fetchone()[0]
    
    cur.execute("SELECT count(*) FROM active_members WHERE private_key IS NOT NULL AND length(private_key) > 10")
    with_keys = cur.fetchone()[0]
    
    print(f"   📊 TOTAL ACCOUNTS:      {total}")
    print(f"   ✅ WITH PRIVATE KEYS:   {with_keys}")
    print(f"   ❌ MISSING KEYS:        {total - with_keys}")
    print("---------------------------------------------------------------------")

    # 2. VIEW SAMPLES (Random 5 + Main Wallets)
    print(f"   {'USER ID':<20} | {'NAME':<20} | {'KEY STATUS'}")
    print("   " + "-"*65)
    
    # Show Main Wallets First
    cur.execute("SELECT user_id, name, private_key FROM active_members WHERE is_system_account = 99 LIMIT 5")
    for uid, name, pkey in cur.fetchall():
        status = "✅ SECURED" if pkey and len(pkey) > 10 else "❌ MISSING"
        print(f"   {uid:<20} | {name[:20]:<20} | {status}")

    print("   " + "-"*65)

    # Show Random Member Samples
    cur.execute("SELECT user_id, name, private_key FROM active_members WHERE is_system_account != 99 ORDER BY RANDOM() LIMIT 7")
    for uid, name, pkey in cur.fetchall():
        status = "✅ SECURED" if pkey and len(pkey) > 10 else "❌ MISSING"
        # Truncate long names for display
        clean_name = name[:20] if name else "NO NAME"
        print(f"   {uid:<20} | {clean_name:<20} | {status}")

    print("=====================================================================")
    print("   Note: 'SECURED' means the Private Key is saved in the database.")
    
    conn.close()

import os
if __name__ == "__main__":
    inspect()
