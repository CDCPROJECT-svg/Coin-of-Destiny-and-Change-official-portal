import sqlite3
from datetime import datetime

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def fix_database_and_run():
    print("--- 🔧 STARTING DATABASE REPAIR ---")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # List of columns to add safely (Name, Type, Default Value)
    columns = [
        ("last_login", "TEXT", "'2026-01-01 00:00:00'"), # Static default to avoid error
        ("status", "TEXT", "'ACTIVE'"),
        ("trading_points", "REAL", "0"),
        ("merchant_points", "REAL", "0"),
        ("channel_points", "REAL", "0"),
        ("watch_hours", "REAL", "0"),
        ("merchant_spend_usdt", "REAL", "0"),
        ("trading_volume_usdt", "REAL", "0")
    ]

    for col_name, col_type, default_val in columns:
        try:
            # Try adding column. If it exists, it will fail cleanly.
            print(f"   👉 Checking column: {col_name}...")
            cur.execute(f"ALTER TABLE active_members ADD COLUMN {col_name} {col_type} DEFAULT {default_val}")
            print(f"      ✅ Added successfully.")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"      ✅ Already exists.")
            else:
                # Ignore other errors if column exists logic is tricky in raw sql
                print(f"      ℹ️ Note: {e}")

    conn.commit()
    conn.close()
    print("✅ DATABASE REPAIR COMPLETE.\n")

    # Now run the simulation logic directly
    print("--- 🚀 LAUNCHING SIMULATION ---")
    import simulation_test
    simulation_test.run_simulation()

if __name__ == "__main__":
    fix_database_and_run()
