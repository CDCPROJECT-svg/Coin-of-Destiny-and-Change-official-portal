import sqlite3
import os

def deep_audit():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # List of tables to inspect
        tables = ['active_members', 'secure_vault', 'system_config']
        
        print("\033[H\033[J", end="")
        print("=========================================================")
        print("      🛡️  CODAC MASTER: INTERNAL DATA STRUCTURE")
        print("=========================================================")

        for table in tables:
            print(f"\n[TABLE: {table.upper()}]")
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            
            print(f"{'CID':<4} | {'NAME':<20} | {'TYPE'}")
            print("-" * 40)
            for col in columns:
                print(f"{col[0]:<4} | {col[1]:<20} | {col[2]}")
            
            # Show sample data from system_config
            if table == 'system_config':
                print("\n[!] DATA PREVIEW (system_config):")
                cursor.execute("SELECT * FROM system_config LIMIT 5;")
                rows = cursor.fetchall()
                for row in rows:
                    print(f" 👉 {row}")

        print("=========================================================")
        conn.close()
    except Exception as e:
        print("[-] Error: " + str(e))

if __name__ == "__main__":
    deep_audit()
