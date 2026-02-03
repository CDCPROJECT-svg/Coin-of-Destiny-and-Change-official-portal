import sqlite3
from datetime import datetime, timedelta

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def scan_inactive_members():
    print("--- 🕵️ SCANNING FOR INACTIVE ACCOUNTS (STRICT RULE) ---")
    
    # NEW RULE: 18 Weeks + 18 Days
    # 18 weeks = 126 days
    # + 18 days
    # TOTAL = 144 DAYS (Exact)
    limit_days = 144
    
    # Calculate the exact cut-off date
    time_threshold = datetime.now() - timedelta(days=limit_days)
    
    print(f"📅 Cut-off Threshold: 144 Days No Login")
    print(f"📅 Date Limit: {time_threshold.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👉 Any login OLDER than this date becomes RED FLAG.")

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Find members inactive since the threshold
        query = """
            SELECT user_id, name, last_login 
            FROM active_members 
            WHERE (last_login < ? OR last_login IS NULL)
            AND status != 'RED_FLAG'
        """
        cur.execute(query, (time_threshold,))
        inactive_users = cur.fetchall()

        if not inactive_users:
            print("✅ No inactive accounts found. Everyone is active within 144 days.")
            return

        # Apply RED FLAG
        print(f"\n⚠️ FOUND {len(inactive_users)} ACCOUNTS EXCEEDING 18 WEEKS + 18 DAYS.")
        print("   Action: Marking as RED_FLAG (Inactive)...")
        
        for user in inactive_users:
            user_id = user[0]
            name = user[1]
            last_active = user[2]
            
            print(f"   🚩 FLAGGED: {name} (ID: {user_id}) | Last Active: {last_active}")
            
            cur.execute("UPDATE active_members SET status = 'RED_FLAG' WHERE user_id = ?", (user_id,))
        
        conn.commit()
        print("\n✅ RED FLAG PROTOCOL COMPLETE. These accounts are now skipped in Perfect 20.")

    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    scan_inactive_members()
