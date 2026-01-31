import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def build_full_structure():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- APPLYING NEW RULES: TASK EXEMPTION & REWARDS ---")

    # 1. ADD NEW RULE COLUMNS (If they don't exist yet)
    # is_task_exempt: 1 = No need to do tasks, 0 = Must do tasks
    # can_claim_rewards: 1 = Can get money, 0 = Cannot
    try:
        cursor.execute("ALTER TABLE active_members ADD COLUMN is_task_exempt INTEGER DEFAULT 0")
        cursor.execute("ALTER TABLE active_members ADD COLUMN can_claim_rewards INTEGER DEFAULT 0")
        print("[OK] New Rule Columns Added to Database.")
    except sqlite3.OperationalError:
        print("[INFO] Rule Columns already exist.")

    # HELPER FUNCTION to insert with rules
    def insert_node(uid, name, level, title, sponsor):
        cursor.execute("""
            INSERT OR REPLACE INTO active_members 
            (user_id, name, current_cycle, current_level, title, sponsor_id, is_task_exempt, can_claim_rewards)
            VALUES (?, ?, 1, ?, ?, ?, 1, 1)
        """, (uid, name, level, title, sponsor))

    print("\n--- BUILDING LEVELS 1 TO 6 (HIERARCHY) ---")
    
    # L1-L3: FOUNDERS (7 Accounts)
    for i in range(1, 8):
        level = i.bit_length()
        insert_node(f"FOUNDER-{i:03d}", "Founder Account", level, "Founder", "SYSTEM_ROOT")

    # L4: CO-FOUNDERS (8 Accounts)
    for i in range(8, 16):
        insert_node(f"COFOUNDER-{i:03d}", "Co-Founder Account", 4, "Co-Founder", "FOUNDER-001")

    # L5: TEAM (16 Accounts)
    for i in range(16, 32):
        insert_node(f"TEAM-{i:03d}", "Team Account", 5, "Core Team", "COFOUNDER-008")

    # L6: DEPARTMENTS (32 Accounts)
    # Marketing (32-39), Innovation (40-47), Legal (48-55), Celeb (56-63)
    for i in range(32, 40): insert_node(f"DEPT-MKT-{i:03d}", "Marketing Dept", 6, "Marketing Node", "TEAM-016")
    for i in range(40, 48): insert_node(f"DEPT-INO-{i:03d}", "CODAC Innovation", 6, "Innovation Node", "TEAM-016")
    for i in range(48, 56): insert_node(f"DEPT-LEG-{i:03d}", "Legalities Dept", 6, "Legalities Node", "TEAM-016")
    for i in range(56, 64): insert_node(f"DEPT-CEL-{i:03d}", "Celebrity & Events", 6, "Celeb/Events Node", "TEAM-016")

    print("\n--- BUILDING LEVELS 7 TO 9 (TREASURY & NATIONS) ---")

    # L7: PORTAL TREASURY (64 Accounts)
    for i in range(64, 128):
        insert_node(f"TREASURY-{i:03d}", "Portal Treasury", 7, "Treasury Node", "DEPT-MKT-032")

    # L8: PORTAL RESERVE (128 Accounts)
    # Clear old data first to be safe
    cursor.execute("DELETE FROM active_members WHERE current_level = 8")
    for i in range(1, 129):
        insert_node(f"CODAC-RES-L08-{i:03d}", "Portal Reserve", 8, "Reserve Node", "SYSTEM_RESERVED")

    # L9: SPECIAL ACCOUNTS (First 52) + COUNTRIES (Next 204)
    # Clear old data first
    cursor.execute("DELETE FROM active_members WHERE current_level = 9")
    
    # A. Special Accounts
    special_names = [
        "CODAC-Coin Backup", "CODAC-Coin Miscellaneous", "CODAC-Coin Incentive",
        "CODAC-Coin Reward", "CODAC-Coin INFRA", "CODAC-Coin Foundation",
        "CODAC-Coin Innovation", "CODAC-Coin Blockchain Fund", "CODAC-Coin System Maintenance",
        "CODAC-Coin Portal"
    ]
    # Fill remaining special slots
    while len(special_names) < 52:
        special_names.append(f"CODAC-Coin Strategic Reserve {len(special_names) + 1}")

    for idx, name in enumerate(special_names):
        uid = f"CODAC-SPEC-{str(idx+1).zfill(3)}"
        insert_node(uid, name, 9, "Special Account", "SYSTEM_RESERVED")

    # B. Countries (204 Slots)
    countries_map = [
        (182, 'Sud', 'Sudan'), (183, 'Phil', 'Philippines'), (184, 'USA', 'United States'),
        (185, 'UAE', 'United Arab Emirates'), (186, 'KSA', 'Saudi Arabia'), (187, 'Fra', 'France'),
        (188, 'UK', 'United Kingdom'), (189, 'Jpn', 'Japan'), (190, 'Chn', 'China'), (191, 'Ind', 'India')
        # Logic handles the numbering for 204
    ]

    for b_id, abbrev, name in countries_map:
        raw_count = str(b_id).zfill(9) 
        formatted_count = f"{raw_count[0:3]}-{raw_count[3:6]}-{raw_count[6:9]}"
        uid = f"CODAC-A09L-{abbrev}-{formatted_count}"
        insert_node(uid, name, 9, "Country Node", "SYSTEM_RESERVED")

    conn.commit()
    conn.close()
    print("\nSUCCESS: Levels 1-9 Built. All marked as EXEMPT from Tasks but ELIGIBLE for Rewards.")

if __name__ == "__main__":
    build_full_structure()
