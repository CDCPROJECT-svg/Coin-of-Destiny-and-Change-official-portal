import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def patch_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    print("   🔧 APPLYING DATABASE PATCH...")

    # Listahan ng mga Columns na kailangan nating idagdag
    required_columns = [
        ("locked_balance", "REAL DEFAULT 0.00"),
        ("lock_end_date", "TEXT DEFAULT NULL"),
        ("current_cycle", "INTEGER DEFAULT 1"),
        ("is_milestone_claimed", "INTEGER DEFAULT 0"),
        ("status", "TEXT DEFAULT 'ACTIVE'"),
        ("is_system_account", "INTEGER DEFAULT 0")
    ]

    for col_name, col_type in required_columns:
        try:
            cur.execute(f"ALTER TABLE active_members ADD COLUMN {col_name} {col_type}")
            print(f"   ✅ Added Missing Column: {col_name}")
        except sqlite3.OperationalError:
            print(f"   ℹ️  Column already exists: {col_name}")

    conn.commit()
    conn.close()
    print("   🚀 DATABASE REPAIRED. READY FOR TESTING.")

if __name__ == "__main__":
    patch_database()
