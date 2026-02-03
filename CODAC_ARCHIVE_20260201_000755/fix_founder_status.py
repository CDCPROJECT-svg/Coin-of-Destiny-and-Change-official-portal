import sqlite3
import os

def force_founder_recognition():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🔧 FOUNDER RECOGNITION FIX")
    print("=========================================================")

    target_id = "FOUNDER-001"

    # 1. Check if table exists (Safety)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_tasks (
            user_id TEXT PRIMARY KEY,
            trading_done BOOLEAN DEFAULT 0,
            youtube_done BOOLEAN DEFAULT 0,
            merchant_done BOOLEAN DEFAULT 0,
            tasks_completed_at REAL DEFAULT NULL,
            join_date REAL
        )
    """)

    # 2. FORCE INSERT / UPDATE
    # Ito ang pipilit sa system na tanggapin ang ID mo as DONE (1) sa lahat ng tasks.
    try:
        cursor.execute("""
            INSERT INTO user_tasks (user_id, trading_done, youtube_done, merchant_done, tasks_completed_at, join_date)
            VALUES (?, 1, 1, 1, 0.0, 0.0)
            ON CONFLICT(user_id) DO UPDATE SET
                trading_done = 1,
                youtube_done = 1,
                merchant_done = 1,
                tasks_completed_at = 0.0;
        """, (target_id,))
        
        conn.commit()
        print(f" [✅] SUCCESS: '{target_id}' has been forcibly registered.")
        print(f"      Status: IMMUNE / EXEMPTED")
        print(f"      Tasks: ALL COMPLETED")
    except Exception as e:
        print(f" [❌] ERROR: {e}")

    conn.close()
    print("=========================================================")
    print("      PLEASE RESTART THE WEB SERVER NOW.")
    print("=========================================================")

if __name__ == "__main__":
    force_founder_recognition()
