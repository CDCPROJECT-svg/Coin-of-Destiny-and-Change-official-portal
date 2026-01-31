import sqlite3
import os

def find_missing():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # Hanapin ang mga members na current_level ay 0 o NULL
        cursor.execute("SELECT user_id, name, join_date FROM active_members WHERE current_level = 0 OR current_level IS NULL")
        missing = cursor.fetchall()

        print("\033[H\033[J", end="")
        print("=========================================================")
        print(f"      🕵️  MISSING MEMBERS REPORT ({len(missing)} found)")
        print("=========================================================")
        print(f"{'USER ID':<10} | {'NAME':<20} | {'JOIN DATE'}")
        print("-" * 55)
        
        if not missing:
            print("   ✅ Good News: Lahat ng members ay nasa loob na ng Tree.")
        else:
            for m in missing:
                print(f"{m[0]:<10} | {m[1]:<20} | {m[2]}")

        print("=========================================================")
        print("   STRATEGY:")
        print("   Kung sila ay Founder/Admin accounts, normal lang ito.")
        print("   Kung regular members sila, kailangan silang i-inject.")
        print("=========================================================")
        
        conn.close()
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    find_missing()
