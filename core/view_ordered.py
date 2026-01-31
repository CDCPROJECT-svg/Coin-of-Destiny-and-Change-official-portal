import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def view_by_slot():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- VIEWING LEVEL 9 BY SLOT ORDER ---")
    
    # We order by 'rowid' which shows exactly who was inserted 1st, 2nd, 3rd...
    cursor.execute("""
        SELECT user_id, name 
        FROM active_members 
        WHERE current_level = 9 
        ORDER BY rowid ASC
    """)
    
    rows = cursor.fetchall()
    
    print(f"{'SLOT':<5} | {'USER ID':<30} | {'NAME'}")
    print("-" * 60)
    
    for i, row in enumerate(rows):
        # We only show the first 60 entries to keep the screen clean
        # (Top 52 Special + First 8 Countries)
        if i >= 60: 
            print("... (Remaining countries follow below) ...")
            break
            
        slot_num = i + 1
        print(f"{slot_num:<5} | {row[0]:<30} | {row[1]}")

    conn.close()

if __name__ == "__main__":
    view_by_slot()
