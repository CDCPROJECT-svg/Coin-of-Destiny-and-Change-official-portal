import sqlite3
import os

def view_raw():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Direct selection of the specific columns you requested
        cursor.execute("SELECT user_id, password, private_key FROM active_members LIMIT 5;")
        rows = cursor.fetchall()

        print("\nID         | PASSWORD (Col 44)   | PRIVATE_KEY (Col 45)")
        print("-" * 75)
        for row in rows:
            print(f"{row[0]:<10} | {row[1]:<18} | {row[2]}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    view_raw()
