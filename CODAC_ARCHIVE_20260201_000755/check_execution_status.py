import sqlite3
import os

def check_status():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # 1. Check how many members have been assigned to a level
        cursor.execute("SELECT COUNT(*) FROM active_members WHERE current_level > 0")
        leveled_members = cursor.fetchone()[0]
        
        # 2. Check the maximum depth currently reached
        cursor.execute("SELECT MAX(current_level) FROM active_members")
        max_depth = cursor.fetchone()[0]
        
        # 3. Check for total points distributed
        cursor.execute("SELECT SUM(codac_points) FROM active_members")
        total_points = cursor.fetchone()[0]

        print("\033[H\033[J", end="")
        print("=========================================================")
        print("      📊 SYSTEM EXECUTION AUDIT STATUS")
        print("=========================================================")
        print(f" [+] Members Processed into Tree : {leveled_members} / 531")
        print(f" [+] Deepest Level Reached       : Level {max_depth if max_depth else 0}")
        print(f" [+] Total CODAC Points Issued   : {total_points if total_points else 0}")
        print("-" * 57)
        
        if leveled_members == 0:
            print(" [!] RESULT: The Core Engine has NOT run yet.")
        elif leveled_members < 531:
            print(" [!] RESULT: Partial execution detected.")
        else:
            print(" [!] RESULT: Full tree population detected.")
        print("=========================================================")
        
        conn.close()
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    check_status()
