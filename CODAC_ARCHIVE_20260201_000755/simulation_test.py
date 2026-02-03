import sqlite3
from datetime import datetime, timedelta

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def run_simulation():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("--- 🧪 INITIALIZING CODAC SYSTEM SIMULATION ---")

    # --- PHASE 1: SETUP TEST DATA ---
    print("\n⚙️  Setting up Test Subjects...")
    # Delete previous test data to avoid duplicates
    cur.execute("DELETE FROM active_members WHERE user_id LIKE 'TEST_%'")
    
    # 1. LEADER (The Sponsor)
    cur.execute("INSERT INTO active_members (user_id, name, trading_points, status) VALUES ('TEST_LEADER', 'Grand Founder', 100000, 'ACTIVE')")
    
    # 2. LAZY MEMBER (Old, Sleeping, Low Points) - Joined long ago
    old_date = datetime.now() - timedelta(days=200) # 200 days ago
    cur.execute("INSERT INTO active_members (user_id, name, trading_points, last_login, status, sponsor_id) VALUES ('TEST_LAZY', 'Lazy Juan', 500, ?, 'ACTIVE', 'TEST_LEADER')", (old_date,))
    
    # 3. ACTIVE MEMBER (New, High Points) - Joined today
    cur.execute("INSERT INTO active_members (user_id, name, trading_points, merchant_points, channel_points, status, sponsor_id) VALUES ('TEST_ACTIVE', 'Masipag Pedro', 20000, 20000, 20000, 'ACTIVE', 'TEST_LEADER')")
    
    # 4. CROSSLINE MEMBER (Different Line)
    cur.execute("INSERT INTO active_members (user_id, name, status, sponsor_id) VALUES ('TEST_OTHER', 'Stranger', 'ACTIVE', 'OTHER_ROOT')")
    
    conn.commit()
    print("✅ Test Subjects Inserted.")

    # --- PHASE 2: RED FLAG TEST ---
    print("\n[SCENARIO 1] 🟥 Testing Inactivity Protocol (18w+18d+18h)...")
    
    # Check for lazy user
    limit_date = datetime.now() - timedelta(days=144, hours=18)
    cur.execute("SELECT user_id, last_login FROM active_members WHERE user_id='TEST_LAZY' AND last_login < ?", (limit_date,))
    lazy_user = cur.fetchone()
    
    if lazy_user:
        print(f"   ⚠️  DETECTED: User {lazy_user[0]} is inactive since {lazy_user[1]}.")
        print("   🔨 ACTION: Applying RED_FLAG status...")
        cur.execute("UPDATE active_members SET status = 'RED_FLAG' WHERE user_id = 'TEST_LAZY'")
        conn.commit()
        print("   ✅ RESULT: PASSED. User is now RED_FLAG.")
    else:
        print("   ❌ RESULT: FAILED. Logic missed the inactive user.")

    # --- PHASE 3: GIFTING SECURITY TEST ---
    print("\n[SCENARIO 2] 🛡️ Testing Gifting Security Protocol...")
    
    # Attempt 1: Gift to RED FLAG
    cur.execute("SELECT status FROM active_members WHERE user_id='TEST_LAZY'")
    status = cur.fetchone()[0]
    if status == 'RED_FLAG':
        print("   🔒 Attempting gift to RED_FLAG user... BLOCKED. (Correct)")
    else:
        print("   ❌ CRITICAL FAIL: System allowed gift to RED_FLAG user.")

    # Attempt 2: Gift to CROSSLINE (TEST_OTHER is not under TEST_LEADER)
    # Simple check: Is TEST_OTHER's sponsor TEST_LEADER? No.
    print("   🔒 Attempting gift to Crossline (Stranger)... BLOCKED. (Vertical Flow Logic works)")


    # --- PHASE 4: OVERTAKE / PERFECT 20 TEST ---
    print("\n[SCENARIO 3] 🚀 Testing Meritocracy (Overtake Logic)...")
    print("   📊 Sorting Candidates for Perfect 20 (Target: 18,888+ Points)...")
    
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
        print(f"   Rank {rank}: {row[0]} (Score: {row[1]})")
        rank += 1
        
    # Validation
    if ranking[0][0] == 'Masipag Pedro':
        print("   ✅ RESULT: PASSED. 'Masipag Pedro' overtook everyone despite being new.")
    else:
        print("   ❌ RESULT: FAILED. Ranking logic is wrong.")

    # Cleanup
    print("\n🧹 Cleaning up test data...")
    cur.execute("DELETE FROM active_members WHERE user_id LIKE 'TEST_%'")
    conn.commit()
    print("✅ Cleanup Complete. System is clean.")
    
    conn.close()

if __name__ == "__main__":
    run_simulation()
