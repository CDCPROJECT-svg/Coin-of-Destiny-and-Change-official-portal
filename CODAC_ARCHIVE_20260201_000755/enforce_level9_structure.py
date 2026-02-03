import sqlite3
import os

def enforce_structure():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🏗️ ARCHITECTURE ENFORCEMENT: LEVEL 9")
    print("=========================================================")

    # 1. IDENTIFY COUNTRIES (Based on CODAC-A09L code)
    cursor.execute("SELECT user_id FROM active_members WHERE user_id LIKE 'CODAC-A09L%'")
    countries = cursor.fetchall()
    
    if not countries:
        print(" [❌] No Country Nodes found. Please restore from Backup if needed.")
        return

    print(f" [1] Found {len(countries)} Countries. Moving them to Level 9...")

    # 2. UPDATE LEVEL AND STATUS
    # We force them to Level 9 regardless of their current parent
    cursor.execute("""
        UPDATE active_members 
        SET current_level = 9, 
            status = 'COUNTRY_ANCHOR',
            position = 'AUTO'
        WHERE user_id LIKE 'CODAC-A09L%'
    """)
    
    # 3. LINKING LOGIC (Optional: Ensure they have parents from Level 8)
    # For now, we just ensure they are tagged correctly for the visualizer.

    conn.commit()
    conn.close()

    print("-" * 57)
    print(" [✅] SUCCESS: All Countries are now locked at LEVEL 9.")
    print("=========================================================")

if __name__ == "__main__":
    enforce_structure()
