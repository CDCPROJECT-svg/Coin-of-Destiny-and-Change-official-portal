import sqlite3
from datetime import datetime, timedelta

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def run_final_test():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("--- 🧪 FINAL SYSTEM VALIDATION ---")

    # --- CLEANUP & SETUP ---
    cur.execute("DELETE FROM active_members WHERE user_id LIKE 'TEST_%'")
    
    # 1. LEADER (Old, but complacent) - 50,000 Points
    cur.execute("INSERT INTO active_members (user_id, name, trading_points, merchant_points, channel_points, status) VALUES ('TEST_LEADER', 'Old Founder', 20000, 20000, 10000, 'ACTIVE')")
    
    # 2. LAZY MEMBER (Inactive 145 Days)
    # Rule: 144 Days Limit. We set to 145 days ago.
    old_date = datetime.now() - timedelta(days=145)
    old_date_str = old_date.strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO active_members (user_id, name, trading_points, last_login, status) VALUES ('TEST_LAZY', 'Lazy Juan', 500, ?, 'ACTIVE')", (old_date_str,))
    
    # 3. MASIPAG PEDRO (New, Super Active) - 200,000 TOTAL POINTS
    # He overtakes everyone.
    cur.execute("INSERT INTO active_members (user_id, name, trading_points, merchant_points, channel_points, status) VALUES ('TEST_ACTIVE', 'Masipag Pedro', 70000, 70000, 60000, 'ACTIVE')")
    
    conn.commit()

    # --- TEST 1: STRICT 144-DAY RED FLAG ---
    print("\n[TEST 1] 🟥 144-Day Red Flag Rule...")
    limit_date = datetime.now() - timedelta(days=144)
    limit_str = limit_date.strftime("%Y-%m-%d %H:%M:%S")
    
    # Find inactive
    cur.execute("SELECT user_id FROM active_members WHERE user_id='TEST_LAZY' AND last_login < ?", (limit_str,))
    if cur.fetchone():
        print("   ✅ DETECTED: Lazy Juan exceeded 144 days.")
        cur.execute("UPDATE active_members SET status = 'RED_FLAG' WHERE user_id = 'TEST_LAZY'")
        conn.commit()
    else:
        print("   ❌ FAILED: Did not detect inactive user.")

    # --- TEST 2: MERITOCRACY (OVERTAKE) ---
    print("\n[TEST 2] 🚀 Overtake Logic (Highest Points First)...")
    
    query = """
        SELECT name, (trading_points + merchant_points + channel_points) as total 
        FROM active_members 
        WHERE user_id LIKE 'TEST_%' AND status != 'RED_FLAG'
        ORDER BY total DESC
    """
    cur.execute(query)
    ranking = cur.fetchall()
    
    rank = 1
    for row in ranking:
        print(f"   Rank {rank}: {row[0]} (Score: {row[1]:,.0f})")
        rank += 1
        
    if ranking[0][0] == 'Masipag Pedro':
        print("   ✅ SUCCESS: 'Masipag Pedro' is #1 (Overtook the Founder!)")
    else:
        print("   ❌ FAILED: Ranking logic error.")

    # Cleanup
    cur.execute("DELETE FROM active_members WHERE user_id LIKE 'TEST_%'")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_final_test()
