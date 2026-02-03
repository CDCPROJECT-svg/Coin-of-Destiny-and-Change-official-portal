import sqlite3
import os
import shutil

def migrate_real_data():
    # PATHS
    source_db = "mother_tree.db"  # Ang luma (Root folder)
    target_db = os.path.expanduser("~/codac-coin_portal/database/codac_master.db") # Ang bago (Database folder)

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      📦 DATA MIGRATION PROTOCOL")
    print(f"      Source: {source_db}")
    print(f"      Target: {target_db}")
    print("=========================================================")

    if not os.path.exists(source_db):
        print(" [❌] CRITICAL: mother_tree.db NOT FOUND in current folder!")
        return

    # CONNECT TO BOTH DATABASES
    try:
        src_conn = sqlite3.connect(source_db)
        src_cursor = src_conn.cursor()
        
        tgt_conn = sqlite3.connect(target_db)
        tgt_cursor = tgt_conn.cursor()
    except Exception as e:
        print(f" [❌] Connection Error: {e}")
        return

    # 1. MIGRATE VIPS (FOUNDER/COFOUNDER)
    print("\n [1] MIGRATING VIP ACCOUNTS (Level 1-9)...")
    try:
        # Check table name in old DB (usually 'users' or 'active_members')
        # We try 'active_members' first, if fail, try 'users'
        table_name = "active_members"
        try:
            src_cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        except:
            table_name = "users" # Fallback
            
        print(f"     (Reading from table: '{table_name}')")

        # Select Real VIPs
        query = f"SELECT user_id, parent_id, position, current_level FROM {table_name} WHERE user_id LIKE 'FOUNDER-%' OR user_id LIKE 'VIP-%' OR user_id LIKE 'COFOUNDER-%'"
        src_cursor.execute(query)
        vips = src_cursor.fetchall()
        
        count_vip = 0
        for v in vips:
            # Insert into New DB
            tgt_cursor.execute("""
                INSERT OR REPLACE INTO active_members (user_id, parent_id, position, current_level, current_cycle, status)
                VALUES (?, ?, ?, ?, 1, 'VIP_MIGRATED')
            """, (v[0], v[1], v[2], v[3]))
            count_vip += 1
            
        print(f"     ✅ Successfully Migrated: {count_vip} VIPs")

    except Exception as e:
        print(f"     ⚠️ VIP Migration Issue: {e}")

    # 2. MIGRATE COUNTRIES (Sudan, France, etc.)
    print("\n [2] MIGRATING 204 COUNTRIES...")
    try:
        # Select Countries
        query = f"SELECT user_id FROM {table_name} WHERE user_id LIKE 'COUNTRY-%' OR user_id = 'SUDAN' OR user_id = 'FRANCE'"
        src_cursor.execute(query)
        countries = src_cursor.fetchall()
        
        count_country = 0
        for c in countries:
            tgt_cursor.execute("""
                INSERT OR REPLACE INTO active_members (user_id, parent_id, position, current_level, current_cycle, status)
                VALUES (?, 'SYSTEM', 'AUTO', 1, 1, 'COUNTRY_NODE')
            """, (c[0],))
            count_country += 1
            
        print(f"     ✅ Successfully Migrated: {count_country} Countries")

    except Exception as e:
        print(f"     ⚠️ Country Migration Issue: {e}")

    # COMMIT AND CLOSE
    tgt_conn.commit()
    src_conn.close()
    tgt_conn.close()

    print("-" * 57)
    print(" [🚀] MIGRATION COMPLETE.")
    print("      Your real data is now inside the Portal Database.")
    print("=========================================================")

if __name__ == "__main__":
    migrate_real_data()
