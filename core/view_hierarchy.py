import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def view_level():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- CODAC HIERARCHY VIEWER ---")
    print("Available Levels: 1 to 9")
    try:
        target_level = int(input("Enter Level to View: "))
    except ValueError:
        print("Invalid number.")
        return

    print(f"\n--- LISTING MEMBERS IN LEVEL {target_level} ---")
    
    # Select data including the new Rule Columns
    cursor.execute("""
        SELECT user_id, name, title, is_task_exempt, can_claim_rewards 
        FROM active_members 
        WHERE current_level = ? 
        ORDER BY user_id ASC
    """, (target_level,))
    
    rows = cursor.fetchall()
    
    if not rows:
        print("No members found in this level.")
    else:
        print(f"{'USER ID':<25} | {'NAME':<30} | {'EXEMPT?':<8} | {'REWARDS?'}")
        print("-" * 85)
        for row in rows:
            uid, name, title, exempt, reward = row
            # Convert 1/0 to Yes/No for easier reading
            is_exempt = "YES" if exempt == 1 else "NO"
            can_reward = "YES" if reward == 1 else "NO"
            
            print(f"{uid:<25} | {name:<30} | {is_exempt:<8} | {can_reward}")

    print("-" * 85)
    print(f"Total in Level {target_level}: {len(rows)}")
    conn.close()

if __name__ == "__main__":
    view_level()
