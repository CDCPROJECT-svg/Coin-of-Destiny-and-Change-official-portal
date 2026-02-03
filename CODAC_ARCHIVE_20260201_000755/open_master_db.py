import sqlite3
import os

def open_master_vault():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🗄️ OPENING CODAC MASTER DATABASE")
    print(f"      Target: {db_path}")
    print("=========================================================")

    if not os.path.exists(db_path):
        print(" [❌] ERROR: Database file does not exist!")
        return

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 1. CHECK ACTIVE_MEMBERS TABLE (The People/Countries)
        print("\n [1] CHECKING 'active_members' TABLE:")
        try:
            # Count Total
            cursor.execute("SELECT COUNT(*) FROM active_members")
            total = cursor.fetchone()[0]
            print(f"      📊 Total Records: {total}")

            # Check FOUNDER
            cursor.execute("SELECT * FROM active_members WHERE user_id='FOUNDER-001'")
            founder = cursor.fetchone()
            if founder:
                print(f"      ✅ FOUNDER-001 is PRESENT.")
                print(f"         (Level: {founder['current_level']}, Cycle: {founder['current_cycle']})")
            else:
                print(f"      ❌ FOUNDER-001 is MISSING.")

            # Check for VIPs (Sample)
            cursor.execute("SELECT COUNT(*) FROM active_members WHERE user_id LIKE 'FOUNDER-%' AND user_id != 'FOUNDER-001'")
            vip_count = cursor.fetchone()[0]
            print(f"      📊 VIP/Downline Accounts: {vip_count}")

            # Check for COUNTRIES (Sudan/France)
            print("      🌍 Country Check:")
            countries_to_check = ['SUDAN', 'FRANCE', 'PHILIPPINES']
            for c in countries_to_check:
                cursor.execute(f"SELECT user_id FROM active_members WHERE user_id LIKE '%{c}%'")
                res = cursor.fetchone()
                if res:
                    print(f"         ✅ Found: {res['user_id']}")
                else:
                    print(f"         ❌ Missing: {c}")

        except sqlite3.OperationalError as e:
            print(f"      [⚠️] Error reading active_members: {e}")

        # 2. CHECK USER_TASKS (The Immunity/Race)
        print("\n [2] CHECKING 'user_tasks' TABLE (Immunity Status):")
        try:
            cursor.execute("SELECT * FROM user_tasks WHERE user_id='FOUNDER-001'")
            task = cursor.fetchone()
            if task:
                status = "IMMUNE/DONE" if task['tasks_completed_at'] == 0.0 else "NORMAL"
                print(f"      ✅ FOUNDER Task Status: {status}")
            else:
                print(f"      ❌ FOUNDER has no task record.")
        except:
            print("      [⚠️] user_tasks table might be missing.")

        conn.close()

    except Exception as e:
        print(f" [❌] CRITICAL ERROR: Database might be corrupted. \n      Details: {e}")

    print("=========================================================")
    print("      REVIEW COMPLETE.")
    print("=========================================================")

if __name__ == "__main__":
    open_master_vault()
