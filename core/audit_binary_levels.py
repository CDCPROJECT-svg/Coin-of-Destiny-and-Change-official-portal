import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def audit_levels():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n" + "="*60)
    print("      CODAC BINARY TREE AUDIT: LEVELS 1 - 9")
    print("="*60)

    # Note: Dahil wala pa tayong 'binary_tree' table, titingnan natin sa 'active_members'
    # kung paano sila naka-sequence base sa user_id (Positioning Logic).
    
    try:
        # Check total country nodes
        cursor.execute("SELECT count(*) FROM active_members WHERE user_id LIKE 'CODAC-A09L%'")
        total_countries = cursor.fetchone()[0]
        
        print(f"Total Countries Available for Tree: {total_countries}")
        print("-" * 60)

        # Simulation/Check of Level Distribution
        # Level 1: 1 node (Root)
        # Level 2: 2 nodes
        # Level 3: 4 nodes... up to Level 8 (128) and part of Level 9.
        
        current_idx = 0
        cursor.execute("SELECT name FROM active_members WHERE user_id LIKE 'CODAC-A09L%' ORDER BY gdp_tier ASC, user_id ASC")
        all_members = cursor.fetchall()

        for level in range(1, 10):
            nodes_in_level = 2**(level-1)
            level_members = all_members[current_idx : current_idx + nodes_in_level]
            
            print(f"LEVEL {level}: ({len(level_members)} / {nodes_in_level} nodes populated)")
            
            if level_members:
                # Print first 2 countries in this level
                names = [m[0] for m in level_members[:2]]
                print(f"   Nodes: {', '.join(names)} {'...' if len(level_members) > 2 else ''}")
            else:
                print("   Nodes: EMPTY")
            
            current_idx += nodes_in_level
            if current_idx >= total_countries:
                break

    except Exception as e:
        print(f"Error: {e}")

    conn.close()

if __name__ == "__main__":
    audit_levels()
