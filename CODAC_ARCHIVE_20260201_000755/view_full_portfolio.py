import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def scan_wallets():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="")
    print("==================================================================================")
    print("           💼 CODAC PORTAL: FULL WALLET BREAKDOWN (PER ID)")
    print("==================================================================================")
    # Header
    print(f" {'PORTAL ID':<18} | {'CODAC WALLET':<15} | {'USDT WALLET':<15} | {'LOCKED VAULT':<15}")
    print("----------------------------------------------------------------------------------")

    # Kuhanin pati USDT balance
    cur.execute("""
        SELECT user_id, trading_points, usdt_balance, locked_balance 
        FROM active_members 
        ORDER BY is_system_account DESC, user_id ASC
    """)
    
    rows = cur.fetchall()
    
    for row in rows:
        uid, codac, usdt, lock = row
        # Safety check kung null
        codac = codac if codac else 0.0
        usdt = usdt if usdt else 0.0
        lock = lock if lock else 0.0
        
        print(f" {uid:<18} | {codac:<15,.2f} | {usdt:<15,.2f} | {lock:<15,.2f}")

    print("==================================================================================")
    print("  NOTE: This view includes the Cash Wallet (USDT) and Security Vaults.")
    print("==================================================================================")
    conn.close()

if __name__ == "__main__":
    scan_wallets()
