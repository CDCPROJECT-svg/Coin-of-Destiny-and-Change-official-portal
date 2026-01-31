import sqlite3
import os

def check_real_vips():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    
    if not os.path.exists(db_path):
        print(" [❌] ERROR: Database file missing!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🔍 CODAC VIP CENSUS (DATABASE INSPECTION)")
    print("=========================================================")

    # 1. COUNT TOTAL MEMBERS
    cursor.execute("SELECT COUNT(*) FROM active_members")
    total = cursor.fetchone()[0]
    print(f" [📊] TOTAL ACCOUNTS IN DB: {total}")

    # 2. CHECK FOUNDER'S DIRECT DOWNLINES (Level 1)
    print("\n [👑] CHECKING FOUNDER'S DIRECT LINES (Level 1):")
    cursor.execute("SELECT user_id, position FROM active_members WHERE parent_id='FOUNDER-001'")
    directs = cursor.fetchall()
    
    if directs:
        for d in directs:
            print(f"      -> Found: {d[0]} ({d[1]})")
    else:
        print("      [⚠️] WARNING: No direct downlines found under FOUNDER-001.")

    # 3. SCAN FOR EXISTING VIPs (Level 1 to 9)
    print("\n [🕵️] SCANNING FOR VIP NETWORK...")
    # We look for anyone who is NOT the Founder or System Wallets
    cursor.execute("""
        SELECT user_id, current_level 
        FROM active_members 
        WHERE user_id NOT IN ('FOUNDER-001', 'COLLECTOR-001', 'RESERVE-WALLET', 'CODAC-OFFICIAL')
        LIMIT 10
    """)
    vips = cursor.fetchall()
    
    if vips:
        print(f"      Sample Existing IDs found:")
        for v in vips:
            print(f"      - {v[0]} (Level {v[1]})")
        print(f"\n      ...and more.")
    else:
        print("      [⚠️] CRITICAL: The VIP Accounts seem to be MISSING from this specific DB file.")
        print("      (Did the previous 'Purge' delete them?)")

    conn.close()
    print("=========================================================")

if __name__ == "__main__":
    check_real_vips()
