import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def list_countries():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n--- CURRENT COUNTRY LIST (196 FOUND) ---")
    cursor.execute("SELECT name FROM active_members WHERE user_id LIKE 'CODAC-A09L%' ORDER BY name ASC")
    countries = cursor.fetchall()
    
    # Print in columns
    for i in range(0, len(countries), 3):
        row = countries[i:i+3]
        print(f"{row[0][0]:<25} {row[1][0] if len(row)>1 else '':<25} {row[2][0] if len(row)>2 else ''}")

    print("\n" + "="*60)
    print(f"TOTAL COUNT: {len(countries)}")
    print("MISSING: 8 Countries to reach 204.")
    print("="*60)
    conn.close()

if __name__ == "__main__":
    list_countries()
