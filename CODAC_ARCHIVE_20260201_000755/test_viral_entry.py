import sqlite3
import os

def simulate_new_entry():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🧪 VIRAL ENGINE TEST: NEW MEMBER ENTRY")
    print("=========================================================")

    # 1. FIND PHILIPPINES (PH)
    # Target Code from your list: CODAC-A09L-Phi...
    target_pattern = "CODAC-A09L-Phi%" 
    
    cursor.execute("SELECT user_id, current_level FROM active_members WHERE user_id LIKE ? LIMIT 1", (target_pattern,))
    country = cursor.fetchone()
    
    if not country:
        print(" [❌] Philippines node not found! Using fallback...")
        # Fallback to ANY country if PH is missing for some reason
        cursor.execute("SELECT user_id, current_level FROM active_members WHERE user_id LIKE 'CODAC-A09L%' LIMIT 1")
        country = cursor.fetchone()
    
    parent_id = country[0]
    parent_level = country[1]

    print(f" [🎯] TARGET ANCHOR: {parent_id}")
    print(f"      (Country Node Level: {parent_level})")

    # 2. CREATE NEW MEMBER (JUAN)
    new_member_id = "MEMBER-JUAN-DELACRUZ"
    
    print(f"\n [👤] INCOMING USER: {new_member_id}")
    print("      Action: Signing up via Global Invite Link...")

    # Insert Logic
    try:
        cursor.execute("""
            INSERT INTO active_members (user_id, parent_id, position, current_level, current_cycle, status)
            VALUES (?, ?, 'LEFT', ?, 1, 'PUBLIC_MEMBER')
        """, (new_member_id, parent_id, parent_level + 1))
        
        conn.commit()
        print("-" * 57)
        print(f" [✅] SUCCESS! {new_member_id} joined the network.")
        print(f"      Placed under: {parent_id}")
        print(f"      New Level: {parent_level + 1}")
    except sqlite3.IntegrityError:
        print(f" [⚠️] Member {new_member_id} already exists!")

    conn.close()
    print("=========================================================")

if __name__ == "__main__":
    simulate_new_entry()
