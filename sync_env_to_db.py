import sqlite3
import os

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
ENV_PATH = "/data/data/com.termux/files/home/codac-coin_portal/.env"

def sync_founder_credentials():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🔄 SYNCING .ENV TO DATABASE (FOUNDER-001)")
    print("=========================================================")

    # 1. Check if .env exists
    if not os.path.exists(ENV_PATH):
        print("   ❌ ERROR: .env file not found!")
        return

    # 2. Read .env manually
    env_vars = {}
    with open(ENV_PATH, "r") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                env_vars[key] = value.strip().strip('"').strip("'")

    # 3. Find the Key
    # Tries different common variable names
    founder_key = env_vars.get("PRIVATE_KEY") or env_vars.get("FOUNDER_PRIVATE_KEY") or env_vars.get("FOUNDER_KEY")
    founder_wallet = env_vars.get("WALLET_ADDRESS") or env_vars.get("FOUNDER_WALLET_ADDRESS")

    if not founder_key:
        print("   ❌ No Private Key found inside .env file.")
        print("   (Checked: PRIVATE_KEY, FOUNDER_PRIVATE_KEY, FOUNDER_KEY)")
        return

    print(f"   ✅ FOUND KEY IN .ENV!")
    if founder_wallet:
        print(f"   ✅ FOUND WALLET: {founder_wallet}")
    else:
        print("   ⚠️  No Wallet Address in .env (Will keep existing or null)")

    # 4. Update Database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        # Check if FOUNDER-001 exists
        cur.execute("SELECT name FROM active_members WHERE user_id = 'FOUNDER-001'")
        if not cur.fetchone():
            print("   ⚠️  FOUNDER-001 not found in DB. Creating placeholder...")
            cur.execute("INSERT INTO active_members (user_id, name, is_system_account) VALUES ('FOUNDER-001', 'THE FOUNDER', 1)")

        # Update the Key
        if founder_wallet:
            cur.execute("""
                UPDATE active_members 
                SET private_key = ?, wallet_address = ? 
                WHERE user_id = 'FOUNDER-001'
            """, (founder_key, founder_wallet))
        else:
            cur.execute("""
                UPDATE active_members 
                SET private_key = ? 
                WHERE user_id = 'FOUNDER-001'
            """, (founder_key,))
            
        conn.commit()
        print("-" * 50)
        print("   ✅ SUCCESS: FOUNDER-001 updated with credentials from .env")
        
    except Exception as e:
        print(f"   ❌ Database Error: {e}")

    conn.close()

if __name__ == "__main__":
    sync_founder_credentials()
