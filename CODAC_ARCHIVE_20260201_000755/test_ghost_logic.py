import sqlite3
DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def test_logic():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    print("--- 🧪 TESTING GHOST LOGIC ---")

    # 1. SETUP:
    # - FOUNDER-001 is VIP in Cycle 2 (Should be Ghost)
    # - NEW-MEMBER is Regular in Cycle 1 (Should be Counted)
    
    # Reset for test
    cur.execute("DELETE FROM active_members WHERE user_id LIKE 'TEST_%'")
    
    # Insert VIP (Cycle 2)
    cur.execute("""
        INSERT INTO active_members (user_id, name, is_task_exempt, current_cycle, status)
        VALUES ('TEST_VIP', 'Royal Founder', 1, 2, 'ACTIVE')
    """)
    
    # Insert New Member (Cycle 1)
    cur.execute("""
        INSERT INTO active_members (user_id, name, is_task_exempt, current_cycle, status)
        VALUES ('TEST_NEW', 'New Recruit', 0, 1, 'ACTIVE')
    """)
    
    conn.commit()
    conn.close()

    # 2. RUN AUDIT
    import graduation_engine_smart
    graduation_engine_smart.audit_perfect_20_smart()
    
    # Expected: Total 2, Effective 1.

if __name__ == "__main__":
    test_logic()
