import sqlite3
import os

def migrate_from_recovered():
    # TARGETING THE BACKUP FILE
    source_db = "mother_tree_RECOVERED.db" 
    target_db = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🚑 DATA RESCUE OPERATION")
    print(f"      Source: {source_db} (The Backup)")
    print("=========================================================")

    if not os.path.exists(source_db):
        print(" [❌] ERROR: mother_tree_RECOVERED.db not found!")
        print("      Please check if the file name is correct.")
        return

    try:
        src_conn = sqlite3.connect(source_db)
        src_cursor = src_conn.cursor()
        
        tgt_conn = sqlite3.connect(target_db)
        tgt_cursor = tgt_conn.cursor()
    except Exception as e:
        print(f" [❌] Connection Failed: {e}")
        return

    # 1. RESCUE VIPs (Users Table)
    print("\n [1] ATTEMPTING TO READ VIPs...")
    try:
        # Try finding the table name in the recovered DB
        src_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = src_cursor.fetchall()
        print(f"     Tables found in backup: {[t[0] for t in tables]}")
        
        # Assume 'users' or 'active_members' exists
        target_table = 'users' if ('users',) in tables else 'active_members'
        
        query = f"SELECT user_id, parent_id, position, current_level FROM {target_table} WHERE user_id LIKE 'FOUNDER-%' OR user_id LIKE 'VIP-%' OR user_id LIKE 'COFOUNDER-%'"
        src_cursor.execute(query)
        vips = src_cursor.fetchall()
        
        count = 0
        for v in vips:
            tgt_cursor.execute("""
                INSERT OR REPLACE INTO active_members (user_id, parent_id, position, current_level, current_cycle, status)
                VALUES (?, ?, ?, ?, 1, 'RECOVERED_VIP')
            """, (v[0], v[1], v[2], v[3]))
            count += 1
        print(f"     ✅ RESCUED: {count} VIP Accounts")

    except Exception as e:
        print(f"     ⚠️ VIP Rescue Failed: {e}")

    # 2. RESCUE COUNTRIES
    print("\n [2] ATTEMPTING TO READ COUNTRIES...")
    try:
        query = f"SELECT user_id FROM {target_table} WHERE user_id LIKE 'COUNTRY-%' OR user_id = 'SUDAN' OR user_id = 'FRANCE'"
        src_cursor.execute(query)
        countries = src_cursor.fetchall()
        
        count_c = 0
        for c in countries:
            tgt_cursor.execute("""
                INSERT OR REPLACE INTO active_members (user_id, status, current_level, current_cycle)
                VALUES (?, 'COUNTRY_NODE', 1, 1)
            """, (c[0],))
            count_c += 1
        print(f"     ✅ RESCUED: {count_c} Country Nodes")

    except Exception as e:
        print(f"     ⚠️ Country Rescue Failed: {e}")

    tgt_conn.commit()
    src_conn.close()
    tgt_conn.close()
    print("=========================================================")

if __name__ == "__main__":
    migrate_from_recovered()
