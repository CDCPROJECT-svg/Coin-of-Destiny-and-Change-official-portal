import sqlite3
import os

def view_database_contents():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    cur = conn.cursor()

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🗄️ CODAC MASTER DB: FULL CONTENT REVIEW")
    print("=========================================================")

    # 1. GET ALL TABLE NAMES
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    if not tables:
        print(" [❌] DATABASE IS EMPTY. No tables found.")
        return

    for table in tables:
        table_name = table['name']
        print(f"\n 📂 TABLE: {table_name.upper()}")
        print("-" * 57)

        # 2. GET COLUMN STRUCTURE (SCHEMA)
        cur.execute(f"PRAGMA table_info({table_name})")
        columns = cur.fetchall()
        col_names = [col['name'] for col in columns]
        print(f" [🏗️] COLUMNS: {', '.join(col_names)}")

        # 3. GET ACTUAL DATA (LIMIT TO 5 ROWS)
        print(f" [📝] SAMPLE DATA (First 5 Rows):")
        cur.execute(f"SELECT * FROM {table_name} LIMIT 5")
        rows = cur.fetchall()

        if rows:
            for row in rows:
                # Convert row object to a readable dictionary-like string
                data = dict(row)
                print(f"      -> {data}")
        else:
            print("      [⚠️] Table is currently EMPTY (No records yet).")
        
        print("=" * 57)

    conn.close()
    print("\n [✅] END OF DATABASE REVIEW.")

if __name__ == "__main__":
    view_database_contents()
