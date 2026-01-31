import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def check():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    print("\n   🔍 VERIFYING TRANSACTION RESULTS...\n")

    # Check Founder
    cur.execute("SELECT current_cycle, locked_balance, trading_points FROM active_members WHERE user_id='FOUNDER-001'")
    f = cur.fetchone()
    if f:
        print(f"   👤 FOUNDER-001:")
        print(f"      - New Cycle:  {f[0]} (Target: 2)")
        print(f"      - New Lock:   {f[1]:.2f} (Target: 0.50)")
        print(f"      - New Wallet: {f[2]:.2f} (Target: 9.50)")
    else:
        print("   ❌ Founder not found.")

    # Check Collector
    cur.execute("SELECT trading_points FROM active_members WHERE user_id='COLLECTOR-001'")
    c = cur.fetchone()
    if c:
        print(f"\n   🏦 COLLECTOR-001:")
        print(f"      - Collected Fee: {c[0]:.2f} (Target: 1.00)")

    conn.close()

if __name__ == "__main__":
    check()
