import sqlite3
import os

# Define where the database file will live
DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def create_fresh_db():
    print(f"Initializing Clean Database at: {DB_PATH}")
    
    # Connect (this creates the file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Active Members Table (Current Location)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS active_members (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        current_cycle INTEGER DEFAULT 1,
        current_level INTEGER DEFAULT 1,
        codac_points REAL DEFAULT 0.0,
        title TEXT,
        sponsor_id TEXT,
        join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    print("[OK] Active Members Table created.")

    # 2. Graduation History (The Archive/Receipts)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS graduation_history (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        cycle_completed INTEGER,
        level_completed INTEGER,
        title_earned TEXT,
        points_earned REAL,
        date_graduated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    print("[OK] Graduation History Table created.")

    conn.commit()
    conn.close()
    print("SUCCESS: Database structure is ready.")

if __name__ == "__main__":
    create_fresh_db()
