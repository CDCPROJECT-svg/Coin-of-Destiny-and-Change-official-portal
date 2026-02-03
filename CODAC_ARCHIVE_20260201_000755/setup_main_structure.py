import sqlite3
import os
import binascii

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

MAIN_ACCOUNTS = [
    ("MAIN-RESERVE", "FOUNDER PORTAL RESERVE"),
    ("MAIN-TREASURY", "FOUNDER PORTAL TREASURY"),
    ("MAIN-GLOBAL", "GLOBAL PORTAL REWARD"),
    ("MAIN-SUCCESSION", "SUCCESSION RESERVE"),
    ("MAIN-COFOUNDER", "CO-FOUNDER RESERVE"),
    ("MAIN-MANAGEMENT", "CODAC MAIN MANAGEMENT"),
    ("MAIN-TEAM", "PORTAL TEAM ACCOUNT")
]

def generate_hex(n_bytes):
    return binascii.hexlify(os.urandom(n_bytes)).decode()

def setup():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("Checking and repairing database structure...")

    # 1. FIX: Add 'password' column if missing
    try:
        cur.execute("ALTER TABLE active_members ADD COLUMN password TEXT DEFAULT '123456'")
        print("   ✅ Added missing column: password")
    except: pass

    # 2. Add 'usdt_balance' column if missing
    try:
        cur.execute("ALTER TABLE active_members ADD COLUMN usdt_balance REAL DEFAULT 0.0")
    except: pass

    # 3. Add Wallet Columns if missing
    try:
        cur.execute("ALTER TABLE active_members ADD COLUMN wallet_address TEXT")
    except: pass
    try:
        cur.execute("ALTER TABLE active_members ADD COLUMN private_key TEXT")
    except: pass

    print("Database structure is now correct.")
    print("-" * 50)

    # 4. Create Main Accounts
    for uid, name in MAIN_ACCOUNTS:
        cur.execute("SELECT user_id FROM active_members WHERE user_id = ?", (uid,))
        if not cur.fetchone():
            wallet = "0x" + generate_hex(20)
            pkey = "0x" + generate_hex(32)
            
            cur.execute("""
                INSERT INTO active_members 
                (user_id, name, password, trading_points, usdt_balance, locked_balance, is_system_account, wallet_address, private_key)
                VALUES (?, ?, 'FOUNDER_AUTH', 0.0, 0.0, 0.0, 99, ?, ?)
            """, (uid, name, wallet, pkey))
            print(f"   ✅ CREATED: {name}")
        else:
            print(f"   ℹ️  READY: {name}")

    conn.commit()
    conn.close()
    print("=" * 50)
    print("ALL MAIN WALLETS ARE NOW ACTIVE.")

if __name__ == "__main__":
    setup()
