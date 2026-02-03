import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def upgrade_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("   ⚙️  UPGRADING DATABASE VAULTS...")

    # 1. ADD NEW COLUMNS (Kung wala pa)
    columns = [
        ("usdt_balance", "REAL DEFAULT 0.00"),
        ("grand_reward_total", "REAL DEFAULT 0.00"),
        ("is_system_account", "INTEGER DEFAULT 0") # To identify Treasury, Infra, etc.
    ]
    
    for col, dtype in columns:
        try:
            cur.execute(f"ALTER TABLE active_members ADD COLUMN {col} {dtype}")
            print(f"   ✅ Added Column: {col}")
        except sqlite3.OperationalError:
            print(f"   ℹ️  Column {col} already exists.")

    # 2. CREATE SYSTEM ACCOUNTS (Lagyan natin ng pondo para sa Display)
    system_accounts = [
        ("TREASURY-001", "PORTAL TREASURY", 500000.00),
        ("INCENTIVE-001", "PORTAL INCENTIVES", 100000.00),
        ("INFRA-001", "INFRASTRUCTURE WALLET", 250000.00),
        ("FOUNDATION-001", "CODAC FOUNDATION", 75000.00),
        ("FORFEITED-001", "FORFEITED FUNDS", 0.00),
        ("COUNTRY-PH", "PHILIPPINES WALLET", 50000.00),
        ("BURN-WALLET", "TOTAL BURN", 0.00) # Start clean
    ]

    print("\n   🏦 INITIALIZING SYSTEM ACCOUNTS...")
    for uid, name, initial_fund in system_accounts:
        # Check if exists
        cur.execute("SELECT user_id FROM active_members WHERE user_id = ?", (uid,))
        if not cur.fetchone():
            # Create Account
            cur.execute("""
                INSERT INTO active_members (user_id, name, trading_points, is_system_account, status, current_level, current_cycle)
                VALUES (?, ?, ?, 1, 'SYSTEM', 0, 0)
            """, (uid, name, initial_fund))
            print(f"   ✅ Created {name} ({uid}) with {initial_fund:,.2f}")
        else:
            # Update Fund (Optional: Force update for display)
            cur.execute("UPDATE active_members SET trading_points = ? WHERE user_id = ?", (initial_fund, uid))
            print(f"   🔄 Updated {name}")

    conn.commit()
    conn.close()
    print("\n   🚀 UPGRADE COMPLETE! Your Vaults are ready.")

if __name__ == "__main__":
    upgrade_database()
