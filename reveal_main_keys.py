import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def reveal():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🔐 CODAC MAIN WALLETS - PRIVATE KEY EXPORT")
    print("=========================================================")

    try:
        cur.execute("SELECT name, private_key FROM active_members WHERE is_system_account = 99")
        rows = cur.fetchall()

        if not rows:
            print("\n   ❌ No Main Wallets found. Please run setup first.")
        
        for name, pkey in rows:
            print(f"\n📂 ACCOUNT: {name}")
            print(f"🔑 KEY:     {pkey}")
            print("-" * 57)
            
    except Exception as e:
        print(f"\n   ❌ Error: {e}")

    print("\n⚠️  WARNING: Copy these keys to MetaMask immediately.")
    print("=========================================================")
    conn.close()

if __name__ == "__main__":
    reveal()
