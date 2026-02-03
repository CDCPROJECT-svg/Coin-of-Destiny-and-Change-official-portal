import sqlite3
import time
import os
import sys

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
YOUTUBE_LINK = "https://youtube.com/@codaccoinportalofficialchannel?si=gFR6U1uXkV1Namvf"

def clear():
    try: os.system('clear')
    except: pass

def check_duplicate(cur, email):
    cur.execute("SELECT COUNT(*) FROM active_members WHERE email = ?", (email,))
    if cur.fetchone()[0] > 0:
        return True
    return False

def auto_find_upline(cur):
    # AUTO-FILL LOGIC: Find oldest entry with < 2 downlines
    cur.execute("SELECT user_id, current_level FROM active_members ORDER BY current_level ASC, user_id ASC")
    all_members = cur.fetchall()
    
    for member in all_members:
        upline_id = member[0]
        cur.execute("SELECT COUNT(*) FROM active_members WHERE sponsor_id = ?", (upline_id,))
        count = cur.fetchone()[0]
        if count < 2:
            return upline_id
    return "FOUNDER-001"

def registration_portal():
    clear()
    print("========================================================")
    print("   🌐 CODAC COIN | 1 PERSON 1 ACCOUNT REGISTRATION")
    print("========================================================")
    
    # 1. YOUTUBE CHECK
    print(f"\n   📺 REQUIREMENT: Subscribe to {YOUTUBE_LINK}")
    sub = input("   Subscribed? (YES/NO): ").strip().upper()
    if sub != "YES":
        print("   ❌ REGISTRATION FAILED. Subscribe first.")
        return

    # 2. EMAIL DUPLICATION CHECK
    print("\n   📝 IDENTITY CHECK")
    email = input("   Enter Email Address: ").strip()
    name = input("   Enter Full Name: ").strip()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if check_duplicate(cur, email):
        print("\n   🚫 ACCESS DENIED: This Email is already registered!")
        print("   ⚠️  POLICY: One Person, One Account Only.")
        conn.close()
        return

    # 3. AUTO-PLACEMENT
    print("\n   ⚙️  Scanning Binary Tree for Placement...")
    time.sleep(1)
    upline_id = auto_find_upline(cur)
    
    # Generate ID
    cur.execute("SELECT COUNT(*) FROM active_members")
    count = cur.fetchone()[0]
    new_id = f"MEMBER-{count + 1:04d}"
    
    # Get Level info
    cur.execute("SELECT current_level, current_cycle FROM active_members WHERE user_id=?", (upline_id,))
    up_data = cur.fetchone()
    new_level = up_data[0] + 1
    cycle = up_data[1]

    # 4. CREATE ACCOUNT
    try:
        cur.execute("""
            INSERT INTO active_members 
            (user_id, name, email, sponsor_id, current_level, current_cycle, status, is_kyc_verified, trading_points)
            VALUES (?, ?, ?, ?, ?, ?, 'PENDING_KYC', 0, 0)
        """, (new_id, name, email, upline_id, new_level, cycle))
        conn.commit()
        print("\n   ✅ REGISTRATION SUCCESSFUL!")
        print(f"   👤 New ID: {new_id}")
        print(f"   🌳 Upline: {upline_id}")
        print("   🔒 STATUS: PENDING KYC (Login to Verify)")
    except sqlite3.IntegrityError:
        print("\n   ❌ CRITICAL ERROR: Duplicate Account Detected.")
    
    conn.close()

if __name__ == "__main__":
    registration_portal()
