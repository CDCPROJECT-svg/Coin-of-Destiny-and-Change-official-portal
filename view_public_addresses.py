import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def view_addresses():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="")
    print("=========================================================================")
    print("           📬 CODAC OFFICIAL WALLET ADDRESS DIRECTORY")
    print("=========================================================================")
    print(f" {'PORTAL ID':<18} | {'WALLET ADDRESS (Public)':<42}")
    print("-------------------------------------------------------------------------")

    # Kuhanin ang ID at Address
    try:
        cur.execute("SELECT user_id, wallet_address FROM active_members ORDER BY is_system_account DESC, user_id ASC")
        rows = cur.fetchall()
        
        for row in rows:
            uid, addr = row
            # Kung null, lagyan ng label
            addr = addr if addr else "⚠️ PENDING GENERATION"
            print(f" {uid:<18} | {addr:<42}")
            
    except sqlite3.OperationalError:
        print("\n   ❌ ERROR: Columns not found. Please run the Upgrade Script first.")

    print("=========================================================================")
    print(f"   TOTAL ACCOUNTS: {len(rows)}")
    print("=========================================================================")
    conn.close()

if __name__ == "__main__":
    view_addresses()
