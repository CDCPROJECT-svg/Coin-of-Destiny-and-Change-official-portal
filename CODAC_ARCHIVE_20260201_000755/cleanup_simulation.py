import sqlite3
import os

def clean_database():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🧹 SYSTEM CLEANUP: REMOVING TEST DATA")
    print("=========================================================")

    # 1. Identify Test Data
    target_user = "SIMULATION_USER_001"
    cur.execute("SELECT * FROM active_members WHERE user_id=?", (target_user,))
    exists = cur.fetchone()

    if exists:
        # 2. Delete from Active Members
        cur.execute("DELETE FROM active_members WHERE user_id=?", (target_user,))
        print(f" [🗑️] Deleted Test User: {target_user}")
        
        # 3. Reset any System Configs to Default (Optional, but good practice)
        # We keep the Viral Message because that is official.
        print(" [✅] Viral Message & Links Preserved.")
        
        conn.commit()
        print(" [✨] DATABASE IS NOW CLEAN.")
    else:
        print(" [ℹ️] No test data found. Database is already clean.")

    print("=========================================================")
    conn.close()

if __name__ == "__main__":
    clean_database()
