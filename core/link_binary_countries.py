import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def link_binary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- LINKING COUNTRIES TO BINARY STRUCTURE ---")

    # 1. Add binary columns if they don't exist
    try:
        cursor.execute("ALTER TABLE active_members ADD COLUMN parent_id TEXT")
        cursor.execute("ALTER TABLE active_members ADD COLUMN position TEXT") # 'L' or 'R'
    except sqlite3.OperationalError:
        pass # Columns already exist

    # 2. Get all countries in fixed order
    cursor.execute("SELECT user_id FROM active_members WHERE user_id LIKE 'CODAC-A09L%' ORDER BY gdp_tier ASC, user_id ASC")
    members = [row[0] for row in cursor.fetchall()]

    # 3. Breadth-First Linking (Level by Level)
    for i in range(len(members)):
        left_child_idx = 2 * i + 1
        right_child_idx = 2 * i + 2

        # Link Left Child
        if left_child_idx < len(members):
            cursor.execute("UPDATE active_members SET parent_id = ?, position = 'L' WHERE user_id = ?", 
                           (members[i], members[left_child_idx]))
        
        # Link Right Child
        if right_child_idx < len(members):
            cursor.execute("UPDATE active_members SET parent_id = ?, position = 'R' WHERE user_id = ?", 
                           (members[i], members[right_child_idx]))

    conn.commit()
    print(f"✅ SUCCESS: {len(members)} countries are now linked in the Binary Tree.")
    conn.close()

if __name__ == "__main__":
    link_binary()
