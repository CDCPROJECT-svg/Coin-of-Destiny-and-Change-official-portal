import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def init_rules():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- INITIALIZING CODAC SYSTEM RULES ---")

    # 1. Create system_config Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    # 2. Inject your Depth Rules
    rules = [
        ('MAIN_FEEDING_DEPTH', '28'),
        ('PROJECT_2_17_DEPTH', '25'),
        ('PROJECT_18_DEPTH', '21'),
        ('CURRENT_FEEDING_PHASE', 'I'),
        ('STORAGE_OPTIMIZATION', 'ENABLED')
    ]
    cursor.executemany("INSERT OR REPLACE INTO system_config VALUES (?, ?)", rules)

    # 3. Create extension_tracker Table (For Main Feeding II to Infinite)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS extension_tracker (
            phase_id TEXT PRIMARY KEY,
            parent_phase TEXT,
            start_node_id TEXT,
            status TEXT DEFAULT 'ACTIVE'
        )
    """)
    
    # Initialize Main Feeding I
    cursor.execute("INSERT OR REPLACE INTO extension_tracker (phase_id, status) VALUES ('MAIN_FEEDING_I', 'ACTIVE')")

    conn.commit()
    print("✅ System Config Table: CREATED & RULES INJECTED")
    print("✅ Extension Tracker Table: CREATED")
    print("✅ Main Feeding I: INITIALIZED")
    conn.close()

if __name__ == "__main__":
    init_rules()
