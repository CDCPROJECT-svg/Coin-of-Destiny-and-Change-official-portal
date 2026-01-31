import sqlite3
import os

def extract_and_label():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🌍 OFFICIAL COUNTRY RECOGNITION PROTOCOL")
    print("      Reference: CODAC MASTER LEDGER")
    print("=========================================================")

    # 1. IDENTIFY COUNTRIES (PREFIX: CODAC-A09L)
    # Base sa Image: CODAC-A09L-Afg... = Afghanistan, etc.
    print(" [1] SCANNING FOR 'CODAC-A09L' CODES...")
    
    cursor.execute("""
        SELECT user_id FROM active_members 
        WHERE user_id LIKE 'CODAC-A09L-%'
    """)
    country_nodes = cursor.fetchall()
    
    count = 0
    for node in country_nodes:
        user_id = node[0]
        
        # Determine Status: COUNTRY_NODE
        # This tag pushes them to the bottom of the pyramid later
        cursor.execute("""
            UPDATE active_members 
            SET status = 'COUNTRY_NODE', 
                current_cycle = 1,
                position = 'AUTO'
            WHERE user_id = ?
        """, (user_id,))
        count += 1

    print(f"      ✅ LABELED: {count} Accounts as OFFICIAL COUNTRIES.")

    # 2. IDENTIFY SPECIAL ACCOUNTS (From Directory Image)
    # BIZ-0516 = CODAC TRADING STORE
    # BURN-WALLET = TOTAL BURN
    print("\n [2] LABELING SPECIAL LEDGER ACCOUNTS...")
    
    specials = {
        "BIZ-0516": "TRADING_STORE",
        "BURN-WALLET": "SYSTEM_BURN",
        "COLLECTOR-001": "CYCLE_COLLECTOR",
        "FOUNDATION-001": "CODAC_FOUNDATION"
    }
    
    for uid, role in specials.items():
        # Update if exists
        cursor.execute("""
            UPDATE active_members 
            SET status = ? 
            WHERE user_id = ?
        """, (role, uid))
        print(f"      👉 Updated: {uid} -> {role}")

    conn.commit()
    conn.close()
    
    print("=========================================================")
    print("      EXTRACTION COMPLETE.")
    print("      System now recognizes these IDs as Real Countries.")
    print("=========================================================")

if __name__ == "__main__":
    extract_and_label()
