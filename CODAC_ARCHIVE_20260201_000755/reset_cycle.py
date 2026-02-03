import sqlite3
import os

def reset_founder_to_start():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🔄 CYCLE RESET PROTOCOL")
    print("=========================================================")

    target_id = "FOUNDER-001"
    
    # 1. CHECK CURRENT STATUS
    cursor.execute("SELECT current_cycle FROM active_members WHERE user_id=?", (target_id,))
    before = cursor.fetchone()
    if before:
        print(f" [🧐] Current Status: CYCLE {before[0]}")
    
    # 2. PERFORM RESET
    print(f" [⏳] Resetting {target_id} to Cycle 1...")
    cursor.execute("""
        UPDATE active_members 
        SET current_cycle = 1, 
            current_level = 1,
            grand_reward_total = 0.0 
        WHERE user_id = ?
    """, (target_id,))
    
    conn.commit()
    
    # 3. VERIFY
    cursor.execute("SELECT current_cycle FROM active_members WHERE user_id=?", (target_id,))
    after = cursor.fetchone()
    
    print("-" * 57)
    print(f" [✅] NEW STATUS: CYCLE {after[0]}")
    print("      The Founder is now back to the starting line.")
    print("=========================================================")

    conn.close()

if __name__ == "__main__":
    reset_founder_to_start()
