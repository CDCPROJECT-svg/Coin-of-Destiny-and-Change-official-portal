import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def reveal():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      👁️  LIVE DATABASE CHECK (DIRECT VIEW)")
    print("=========================================================")

    # 1. CHECK FOUNDER-001
    cur.execute("SELECT private_key FROM active_members WHERE user_id = 'FOUNDER-001'")
    founder_key = cur.fetchone()
    
    print(f"\n1. FOUNDER-001 STATUS:")
    if founder_key and founder_key[0] and len(founder_key[0]) > 10:
        print(f"   ✅ KEY FOUND: {founder_key[0][:15]}... (Nasa Database!)")
    else:
        print(f"   ❌ KEY MISSING: {founder_key}")

    # 2. CHECK RANDOM MEMBER (e.g., Albania/Treasury)
    cur.execute("SELECT user_id, private_key FROM active_members WHERE user_id != 'FOUNDER-001' LIMIT 1")
    member = cur.fetchone()
    
    print(f"\n2. SAMPLE MEMBER ({member[0]}) STATUS:")
    if member and member[1] and len(member[1]) > 10:
        print(f"   ✅ KEY FOUND: {member[1][:15]}... (Nasa Database!)")
    else:
        print(f"   ❌ KEY MISSING: {member[1]}")

    conn.close()

if __name__ == "__main__":
    reveal()
