import sqlite3
import os

def investigate_assets():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    csv_path = "cdc_wallets.csv"

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🕵️ CODAC ASSET INVESTIGATION")
    print("=========================================================")

    # 1. IDENTIFY THE 531 MEMBERS IN DATABASE
    print(" [1] WHO ARE THE 531 MEMBERS IN THE DB?")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get a sample of IDs that are NOT the Founder
        cursor.execute("SELECT user_id FROM active_members WHERE user_id != 'FOUNDER-001' LIMIT 20")
        rows = cursor.fetchall()
        
        if rows:
            print("     Here are their IDs (Sample):")
            for r in rows:
                print(f"     - {r[0]}")
        else:
            print("     [?] Weird. Count says 531 but cannot fetch rows.")
            
        conn.close()
    except Exception as e:
        print(f"     [❌] DB Error: {e}")

    # 2. FIND THE COUNTRIES IN THE FILES
    print("\n [2] HUNTING FOR COUNTRIES IN FILES...")
    if os.path.exists(csv_path):
        print(f"     Scanning {csv_path} for 'SUDAN'...")
        found_sudan = False
        try:
            with open(csv_path, 'r', errors='ignore') as f:
                for line in f:
                    if "SUDAN" in line.upper() or "FRANCE" in line.upper():
                        print(f"     ✅ FOUND IN FILE: {line.strip()}")
                        found_sudan = True
                        # Don't break, find a few more
                        if "FRANCE" in line.upper(): break 
            
            if not found_sudan:
                print("     ❌ 'SUDAN' not found in CSV.")
        except:
            print("     [⚠️] Could not read CSV file.")
    else:
        print("     [❌] cdc_wallets.csv is MISSING.")

    print("=========================================================")

if __name__ == "__main__":
    investigate_assets()
