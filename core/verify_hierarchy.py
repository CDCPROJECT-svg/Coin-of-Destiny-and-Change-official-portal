import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def verify():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n" + "="*60)
    print("      CODAC BINARY HIERARCHY VERIFICATION")
    print("="*60)

    # 1. Tingnan ang Root (Level 1)
    cursor.execute("SELECT user_id, name FROM active_members WHERE parent_id IS NULL AND user_id LIKE 'CODAC-A09L%'")
    root = cursor.fetchone()
    if root:
        print(f"ROOT NODE (Level 1): {root[1]} ({root[0]})")
        
        # 2. Tingnan ang Children ng Root (Level 2)
        cursor.execute("SELECT name, position, user_id FROM active_members WHERE parent_id = ?", (root[0],))
        children = cursor.fetchall()
        print("\nCHILDREN of Root (Level 2):")
        for child in children:
            print(f" |-- [{child[1]}] {child[0]} ({child[2]})")
            
            # 3. Tingnan ang Grandchildren (Level 3)
            cursor.execute("SELECT name, position FROM active_members WHERE parent_id = ?", (child[2],))
            g_children = cursor.fetchall()
            for gc in g_children:
                print(f"     |-- [{gc[1]}] {gc[0]}")
    else:
        print("❌ No root found. Hierarchy might be disconnected.")

    # 4. Mag-check ng isang random na bansa sa gitna (e.g., Level 4 or 5)
    print("\n" + "-"*60)
    print("RANDOM NODE CHECK (Mid-Tree):")
    cursor.execute("SELECT name, user_id, parent_id, position FROM active_members WHERE parent_id IS NOT NULL AND user_id LIKE 'CODAC-A09L%' LIMIT 1 OFFSET 50")
    mid = cursor.fetchone()
    if mid:
        # Kunin ang pangalan ng Parent
        cursor.execute("SELECT name FROM active_members WHERE user_id = ?", (mid[2],))
        parent_name = cursor.fetchone()[0]
        print(f"Country: {mid[0]}")
        print(f"Upline (Parent): {parent_name} (Position: {mid[3]})")
        
        # Kunin ang Downlines
        cursor.execute("SELECT name, position FROM active_members WHERE parent_id = ?", (mid[1],))
        downlines = cursor.fetchall()
        print(f"Downlines:")
        for dl in downlines:
            print(f" |-- [{dl[1]}] {dl[0]}")

    conn.close()

if __name__ == "__main__":
    verify()
