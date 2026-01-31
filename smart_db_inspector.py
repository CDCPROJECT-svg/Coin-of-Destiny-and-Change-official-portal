import sqlite3
import os

def find_and_inspect():
    target_db = "Codac_master.db"
    found_path = None
    
    # Deep search within the current project directory
    print("\n[!] Searching for " + target_db + "...")
    for root, dirs, files in os.walk("."):
        if target_db in files:
            found_path = os.path.join(root, target_db)
            break
            
    if not found_path:
        print("[-] Error: " + target_db + " not found in this directory.")
        return

    print("[+] Found Database at: " + found_path)
    
    try:
        # Open in Read-Only mode for safety
        conn = sqlite3.connect(f"file:{found_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print("\n" + "="*50)
        print("      CODAC MASTER DATABASE STRUCTURE")
        print("="*50)
        
        if not tables:
            print("[!] Warning: Database is empty (No tables found).")
        else:
            print(f"{'INDEX':<6} | {'TABLE NAME':<25} | {'RECORDS'}")
            print("-" * 50)
            for i, table in enumerate(tables, 1):
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"{i:<6} | {table[0]:<25} | {count}")

        print("="*50)
        conn.close()
    except Exception as e:
        print("[-] System Error: " + str(e))

if __name__ == "__main__":
    find_and_inspect()
