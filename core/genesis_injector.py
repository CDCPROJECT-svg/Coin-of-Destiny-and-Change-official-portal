import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def inject_genesis():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Founder Details
    genesis_id = "CODAC-2026-01"
    name = "The Founder"
    title = "Ambassador" # Cycle 1, Level 1 Title
    
    try:
        # Insert Founder
        cursor.execute("""
            INSERT INTO active_members 
            (user_id, name, current_cycle, current_level, codac_points, title, sponsor_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (genesis_id, name, 1, 1, 0.0, title, "SYSTEM_ROOT"))
        
        conn.commit()
        print(f"SUCCESS: Genesis Account ({genesis_id}) created.")
        print(f"Rank: {title}")
        
    except sqlite3.IntegrityError:
        print(f"INFO: Genesis Account ({genesis_id}) already exists.")
        
    conn.close()

if __name__ == "__main__":
    inject_genesis()
