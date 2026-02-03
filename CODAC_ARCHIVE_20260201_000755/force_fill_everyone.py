import sqlite3
import os
import binascii

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def generate_hex(n_bytes):
    return binascii.hexlify(os.urandom(n_bytes)).decode()

def force_fill():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      ⚡ ULTIMATE FORCE FILL (EXCEPT FOUNDER-001)")
    print("=========================================================")

    # 1. Kunin LAHAT ng members LIBAN kay Founder-001
    cur.execute("SELECT user_id, name FROM active_members WHERE user_id != 'FOUNDER-001'")
    targets = cur.fetchall()
    
    print(f"   🎯 TARGETS FOUND: {len(targets)} Accounts")
    print("   🚀 Starting Force Injection...")
    print("-" * 50)

    count = 0
    for uid, name in targets:
        # Generate New Credentials
        new_wallet = "0x" + generate_hex(20)
        new_pkey = "0x" + generate_hex(32)
        
        # FORCE UPDATE (Walang IF-IF, Update agad)
        cur.execute("""
            UPDATE active_members 
            SET wallet_address = ?, private_key = ? 
            WHERE user_id = ?
        """, (new_wallet, new_pkey, uid))
        
        count += 1
        if count % 100 == 0:
            print(f"   ... Filled {count} accounts")

    conn.commit()
    print("-" * 50)
    print(f"   ✅ DONE! {count} Accounts have been given keys.")
    
    # FINAL CHECK
    print("\n   🔎 VERIFYING SAMPLE (FOUNDER-002):")
    cur.execute("SELECT private_key FROM active_members WHERE user_id = 'FOUNDER-002'")
    res = cur.fetchone()
    if res and res[0]:
        print(f"   ✅ FOUNDER-002 NOW HAS KEY: {res[0][:10]}...")
    else:
        print("   ❌ STILL FAILED.")

    conn.close()

if __name__ == "__main__":
    force_fill()
