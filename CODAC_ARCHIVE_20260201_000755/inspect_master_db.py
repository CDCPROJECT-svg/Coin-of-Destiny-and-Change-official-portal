import sqlite3
import os

def inspect_master():
    db_path = os.path.expanduser("~/codac-coin_portal/database/Codac_master.db")
    
    if not os.path.exists(db_path):
        # I-check kung nasa main folder ito kung wala sa database folder
        db_path = os.path.expanduser("~/codac-coin_portal/Codac_master.db")

    if not os.path.exists(db_path):
        print("\n❌ Error: Hindi mahanap ang 'Codac_master.db'. Paki-check ang spelling o location.")
        return

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # Kunin ang lahat ng tables sa loob ng database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print("\033[H\033[J", end="")
        print("=========================================================")
        print(f"      🏛️  CODAC MASTER DATABASE STRUCTURE")
        print("=========================================================")
        print(f"   DATABASE: {os.path.basename(db_path)}")
        print(f"   STATUS: Connected (Read-Only Mode)")
        print("-" * 57)

        if not tables:
            print("   ⚠️  BABALA: Walang lamang Tables ang database na ito.")
        else:
            print("   LISTAHAN NG MGA TABLES:")
            for i, table in enumerate(tables, 1):
                # Kunin ang bilang ng records sa bawat table
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"   {i}. {table[0]:<20} | {count} records")

        print("=========================================================")
        print("   Anong Table ang gusto mong busisisiin ang laman?")
        print("=========================================================")
        conn.close()
    except Exception as e:
        print(f"❌ Error during inspection: {e}")

if __name__ == "__main__":
    inspect_master()
