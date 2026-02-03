import sqlite3
import os

def audit_database():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🗄️ CODAC MASTER DATABASE AUDIT")
    print(f"      Path: {db_path}")
    print("=========================================================")
    
    if not os.path.exists(db_path):
        print(" [❌] CRITICAL ERROR: Database file not found!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. LIST ALL TABLES
    print("\n [1] CHECKING TABLES STRUCTURE:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    required_tables = ["active_members", "system_config", "user_tasks"]
    found_tables = [t[0] for t in tables]
    
    for req in required_tables:
        if req in found_tables:
            print(f"      [✅] TABLE FOUND: '{req}'")
        else:
            print(f"      [⚠️] MISSING: '{req}' (Logic exists, but table not yet initialized)")

    # 2. CHECK VIRAL MESSAGE (System Config)
    print("\n [2] CHECKING VIRAL ENGINE CONFIG:")
    try:
        cursor.execute("SELECT value FROM system_config WHERE key='master_viral_msg'")
        msg = cursor.fetchone()
        if msg:
            print("      [✅] Viral Message is SAVED in Database.")
        else:
            print("      [⚠️] Viral Message NOT found.")
    except:
        print("      [⚠️] Config table not readable.")

    # 3. CHECK TASK TRACKING (Race Engine)
    print("\n [3] CHECKING TASK RACE ENGINE:")
    if "user_tasks" in found_tables:
        cursor.execute("SELECT COUNT(*) FROM user_tasks")
        count = cursor.fetchone()[0]
        print(f"      [✅] Task Tracking Active. Records: {count}")
    
    conn.close()
    print("\n=========================================================")
    print("      AUDIT COMPLETE.")
    print("=========================================================")

if __name__ == "__main__":
    audit_database()
