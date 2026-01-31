import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def monitor():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\n=====================================================")
    print("   🏦 CODAC SYSTEM: COLLECTOR WALLET MONITOR")
    print("=====================================================")
    
    # Check Collector-001 Balance
    cur.execute("SELECT trading_points, name FROM active_members WHERE user_id = 'COLLECTOR-001'")
    res = cur.fetchone()
    
    if res:
        balance = res[0]
        name = res[1]
        print(f"   ACCOUNT: {name}")
        print(f"   USER ID: COLLECTOR-001")
        print(f"   BALANCE: {balance:,.4f} CODAC")
        print("-----------------------------------------------------")
        print("   STATUS:  ACTIVE (Receiving Cycle Upgrade Fees)")
    else:
        print("   ⚠️  ERROR: Collector account not found in Database.")

    # Check Total Locked across all members (Potential future collections)
    cur.execute("SELECT SUM(locked_balance) FROM active_members WHERE is_system_account = 0")
    total_locked = cur.fetchone()[0] or 0.00
    print(f"   PENDING LOCKS (In User Vaults): {total_locked:,.2f} CODAC")
    print("=====================================================")
    
    conn.close()

if __name__ == "__main__":
    monitor()
