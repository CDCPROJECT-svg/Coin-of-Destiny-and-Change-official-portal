import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def audit_keys():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🕵️  DATABASE AUDIT REPORT")
    print("=========================================================")

    # 1. Check Total Accounts
    cur.execute("SELECT count(*) FROM active_members")
    total = cur.fetchone()[0]
    
    # 2. Check Valid Keys
    cur.execute("SELECT count(*) FROM active_members WHERE private_key IS NOT NULL AND length(private_key) > 10 AND private_key != 'NOT_GENERATED'")
    with_keys = cur.fetchone()[0]
    
    # 3. Check Empty/Missing
    without_keys = total - with_keys
    
    print(f"   📊 TOTAL ACCOUNTS:      {total}")
    print(f"   ✅ WITH KEYS (Ready):   {with_keys}")
    print(f"   ⚠️  NO KEYS (Empty):     {without_keys}")
    print("=========================================================")

    if with_keys > 0:
        print("   [SAMPLE NA MAY SUSI]")
        cur.execute("SELECT user_id, private_key FROM active_members WHERE length(private_key) > 10 LIMIT 3")
        for uid, key in cur.fetchall():
            print(f"   -> {uid:<18} : {key[:10]}...")

    if without_keys > 0:
        print("\n   [SAMPLE NA WALANG SUSI]")
        cur.execute("SELECT user_id FROM active_members WHERE private_key IS NULL OR length(private_key) < 10 LIMIT 3")
        for row in cur.fetchall():
            print(f"   -> {row[0]:<18} : [BLANK]")
            
    conn.close()

if __name__ == "__main__":
    audit_keys()
