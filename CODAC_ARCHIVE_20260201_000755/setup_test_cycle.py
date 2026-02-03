import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def prepare_test():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    print("   ⚙️  PREPARING TEST SCENARIO...")

    # 1. Reset Founder to Cycle 1
    # Lock = 1.0 (Old Req), Wallet = 10.0 (Budget)
    cur.execute("""
        UPDATE active_members 
        SET current_cycle = 1, 
            locked_balance = 1.00, 
            trading_points = 10.00,
            status = 'ACTIVE'
        WHERE user_id = 'FOUNDER-001'
    """)
    print("   ✅ FOUNDER-001: Ready (Cycle 1, Lock 1.0, Wallet 10.0)")

    # 2. Reset Collector
    cur.execute("UPDATE active_members SET trading_points = 0.00 WHERE user_id = 'COLLECTOR-001'")
    print("   ✅ COLLECTOR-001: Empty (0.00)")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    prepare_test()
