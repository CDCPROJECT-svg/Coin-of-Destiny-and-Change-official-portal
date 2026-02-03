import sqlite3
import os

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
EXPORT_FILE = "/sdcard/Download/CODAC_HIERARCHY_ROOT_TO_LVL9.txt"

def view_hierarchy():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      👑 VIEWING HIERARCHY: ROOT TO LEVEL 9")
    print("=========================================================")

    if not os.path.exists(DB_PATH):
        print("❌ Database not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Query: FOUNDER-001 at lahat ng accounts na may 'lvl' hanggang 9
    # Ginagamit natin ang REGEXP o LIKE para makuha ang tamang levels
    query = """
        SELECT user_id, name, wallet_address, private_key 
        FROM active_members 
        WHERE user_id = 'FOUNDER-001'
        OR user_id LIKE 'lvl-01%'
        OR user_id LIKE 'lvl-02%'
        OR user_id LIKE 'lvl-03%'
        OR user_id LIKE 'lvl-04%'
        OR user_id LIKE 'lvl-05%'
        OR user_id LIKE 'lvl-06%'
        OR user_id LIKE 'lvl-07%'
        OR user_id LIKE 'lvl-08%'
        OR user_id LIKE 'lvl-09%'
        OR (is_system_account = 99 AND name LIKE '%Level%')
        ORDER BY user_id ASC
    """
    
    cur.execute(query)
    rows = cur.fetchall()
    
    total = len(rows)
    print(f"   📊 Found {total} Accounts in Root to Level 9 path.")

    with open(EXPORT_FILE, "w") as f:
        f.write("================================================================\n")
        f.write("   CODAC COIN - ROOT HIERARCHY (FOUNDER TO LEVEL 9)\n")
        f.write(f"   Status: OPEN | Total Nodes: {total}\n")
        f.write("================================================================\n\n")
        
        for row in rows:
            uid, name, addr, key = row
            f.write(f"ID:     {uid}\n")
            f.write(f"NAME:   {name}\n")
            f.write(f"ADDR:   {addr}\n")
            f.write(f"KEY:    {key}\n")
            f.write("-" * 60 + "\n")

    print("-" * 57)
    print("   ✅ SUCCESS! Hierarchy has been extracted.")
    print(f"   📂 File: CODAC_HIERARCHY_ROOT_TO_LVL9.txt")
    print("   📍 Location: Downloads Folder")
    print("=========================================================")

    conn.close()

if __name__ == "__main__":
    view_hierarchy()
