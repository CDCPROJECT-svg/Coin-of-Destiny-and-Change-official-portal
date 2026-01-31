import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def check_endpoints():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n" + "="*60)
    print("      AUDIT: COUNTRIES WITH ZERO DOWNLINES")
    print("="*60)

    # Kunin ang lahat ng countries na hindi parent ng kahit sino
    cursor.execute("""
        SELECT name, user_id FROM active_members 
        WHERE user_id LIKE 'CODAC-A09L%' 
        AND user_id NOT IN (SELECT DISTINCT parent_id FROM active_members WHERE parent_id IS NOT NULL)
    """)
    endpoints = cursor.fetchall()

    print(f"Total Countries at the Frontier (Zero Downlines): {len(endpoints)}")
    print("\nSample of countries waiting for Level 9 members:")
    for row in endpoints[:10]:
        print(f" - {row[0]} ({row[1]})")
    
    # Verify kung exact 102 ang may children (dahil 204/2 = 102)
    cursor.execute("""
        SELECT count(DISTINCT parent_id) FROM active_members 
        WHERE parent_id LIKE 'CODAC-A09L%'
    """)
    parent_count = cursor.fetchone()[0]
    print(f"\nCountries with existing children: {parent_count}")

    conn.close()

if __name__ == "__main__":
    check_endpoints()
