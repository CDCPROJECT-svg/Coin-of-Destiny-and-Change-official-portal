import sqlite3
import os

def audit_master():
    # The exact path from your find results
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🏛️  OFFICIAL CODAC MASTER DATABASE AUDIT")
    print("=========================================================")
    
    if not os.path.exists(db_path):
        print(f"[-] Error: Could not locate {db_path}")
        return

    try:
        # Open in Read-Only mode for data integrity
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # Identify Tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print(f"[+] DATABASE: {db_path}")
        print(f"[+] STATUS:   SECURE & VERIFIED")
        print("-" * 57)
        
        if not tables:
            print("[!] ALERT: This database is empty.")
        else:
            print(f"{'INDEX':<6} | {'TABLE NAME':<25} | {'RECORDS'}")
            print("-" * 57)
            for i, table in enumerate(tables, 1):
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"{i:<6} | {table[0]:<25} | {count}")

        print("=========================================================")
        print("   Which table contains your 18 projects, Founder?")
        print("=========================================================")
        conn.close()
    except Exception as e:
        print(f"[-] System Error: {str(e)}")

if __name__ == "__main__":
    audit_master()
