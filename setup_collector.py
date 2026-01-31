import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def init_collector():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    print("   ⚙️  SETTING UP CYCLE COLLECTOR WALLETS...")

    # Create the Collector Wallet if not exists
    cur.execute("SELECT user_id FROM active_members WHERE user_id='COLLECTOR-001'")
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO active_members (user_id, name, trading_points, is_system_account, status, current_level, current_cycle) 
            VALUES ('COLLECTOR-001', 'CYCLE LOCK COLLECTOR', 0.00, 1, 'SYSTEM', 0, 0)
        """)
        print("   ✅ Created: COLLECTOR-001 (Cycle Vault)")
    else:
        print("   ℹ️  COLLECTOR-001 already exists.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_collector()
