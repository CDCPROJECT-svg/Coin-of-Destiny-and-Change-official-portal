import sqlite3
import os

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
EXPORT_FILE = "/sdcard/Download/CODAC_DATABASE_RAW_DUMP.txt"

def inspect_all():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🔍 RAW DATABASE INSPECTION (ALL RECORDS)")
    print("=========================================================")

    if not os.path.exists(DB_PATH):
        print("❌ Error: Database file not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Kukunin ang LAHAT ng columns at LAHAT ng rows
    cur.execute("SELECT * FROM active_members ORDER BY rowid ASC")
    rows = cur.fetchall()
    
    # Kunin ang column names
    colnames = [description[0] for description in cur.description]

    print(f"   📊 Total Records Found: {len(rows)}")
    
    with open(EXPORT_FILE, "w") as f:
        f.write(f"CODAC MASTER DATABASE DUMP\n")
        f.write(f"Total Entries: {len(rows)}\n")
        f.write("-" * 60 + "\n")
        
        for row in rows:
            for i in range(len(colnames)):
                f.write(f"{colnames[i]}: {row[i]}\n")
            f.write("-" * 30 + "\n")

    print("-" * 57)
    print(f"   ✅ SUCCESS! All records extracted.")
    print(f"   📂 File: CODAC_DATABASE_RAW_DUMP.txt")
    print(f"   📍 Location: Downloads Folder")
    print("=========================================================")
    conn.close()

if __name__ == "__main__":
    inspect_all()
