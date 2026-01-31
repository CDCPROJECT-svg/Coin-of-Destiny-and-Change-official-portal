import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def view_ledgers():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="")
    print("=========================================================================")
    print("          📜 CODAC MASTER LEDGER: ALL WALLETS & PORTAL IDs")
    print("=========================================================================")
    print(f" {'PORTAL ID':<15} | {'NAME/LABEL':<18} | {'WALLET (CODAC)':<15} | {'LOCKED':<8}")
    print("-------------------------------------------------------------------------")

    cur.execute("""
        SELECT user_id, name, trading_points, locked_balance, status 
        FROM active_members 
        ORDER BY is_system_account DESC, user_id ASC
    """)
    
    rows = cur.fetchall()
    for row in rows:
        uid, name, balance, locked, status = row
        # I-format ang display
        print(f" {uid:<15} | {name[:18]:<18} | {balance:<15,.4f} | {locked:<8.2f}")

    print("=========================================================================")
    
    # Summary of System Assets
    cur.execute("SELECT SUM(trading_points), SUM(locked_balance) FROM active_members")
    total_circ, total_lock = cur.fetchone()
    print(f" 🌐 TOTAL CIRCULATION: {total_circ or 0:,.4f} CODAC")
    print(f" 🔒 TOTAL SYSTEM LOCK: {total_lock or 0:,.2f} CODAC")
    print("=========================================================================")

    conn.close()

if __name__ == "__main__":
    view_ledgers()
