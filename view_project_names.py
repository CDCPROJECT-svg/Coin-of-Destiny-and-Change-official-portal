import json
import os
import sqlite3

# PATHS
JSON_PATH = "/data/data/com.termux/files/home/codac-coin_portal/project_roadmap.json"
DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def view_projects():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🏗️  CODAC PROJECT PORTFOLIO VIEWER")
    print("=========================================================")

    # 1. CHECK JSON FILE (Roadmap)
    print("\n[ SOURCE 1: project_roadmap.json ]")
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r") as f:
                data = json.load(f)
                
            # Kung listahan ito
            if isinstance(data, list):
                for idx, proj in enumerate(data):
                    name = proj.get("name", "Unknown Project")
                    status = proj.get("status", "Planned")
                    print(f"   {idx+1}. {name} ({status})")
            
            # Kung dictionary (Project 1, Project 2...)
            elif isinstance(data, dict):
                count = 1
                for key, val in data.items():
                    name = val.get("name") if isinstance(val, dict) else val
                    print(f"   {count}. {key}: {name}")
                    count += 1
            else:
                print("   ⚠️  Format not recognized.")
                
        except Exception as e:
            print(f"   ❌ Error reading JSON: {e}")
    else:
        print("   ❌ File not found: project_roadmap.json")

    # 2. CHECK DATABASE (Active Members with 'PROJECT' tag)
    print("\n[ SOURCE 2: Database (Wallets) ]")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Hahanapin natin ang mga IDs na may "PROJ" o "CYCLE"
    cur.execute("SELECT user_id, name, wallet_address FROM active_members WHERE user_id LIKE 'PROJ%' OR user_id LIKE 'CYCLE%'")
    rows = cur.fetchall()
    
    if rows:
        print(f"   Found {len(rows)} Active Project Wallets:")
        for uid, name, wallet in rows:
            w_display = wallet if wallet else "NO WALLET"
            print(f"   -> {uid:<15} | {name:<20} | {w_display[:10]}...")
    else:
        print("   ⚠️  No Wallets found starting with 'PROJ' or 'CYCLE' in database.")
        print("       (Baka hindi pa sila na-rehistro bilang wallets?)")

    conn.close()
    print("=========================================================")

if __name__ == "__main__":
    view_projects()
