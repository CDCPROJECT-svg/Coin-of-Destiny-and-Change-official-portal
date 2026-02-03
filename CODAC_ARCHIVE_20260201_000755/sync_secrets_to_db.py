import sqlite3
import os
import re

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
SECRETS_PATH = "/data/data/com.termux/files/home/codac-coin_portal/secrets.py"

def hunt_key():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🕵️  KEY HUNTER: SEARCHING secrets.py")
    print("=========================================================")

    # 1. Check if secrets.py exists
    if not os.path.exists(SECRETS_PATH):
        print("   ❌ 'secrets.py' not found.")
        return

    # 2. Scan the file content
    found_key = None
    found_wallet = None
    
    with open(SECRETS_PATH, "r") as f:
        content = f.read()
        
        # Search for patterns like PRIVATE_KEY = "0x..."
        # Regex looks for variable name followed by assignment and a hex string
        key_match = re.search(r'(PRIVATE_KEY|FOUNDER_KEY)\s*=\s*["\'](0x[a-fA-F0-9]{64})["\']', content)
        wallet_match = re.search(r'(WALLET_ADDRESS|FOUNDER_WALLET)\s*=\s*["\'](0x[a-fA-F0-9]{40})["\']', content)

        if key_match:
            found_key = key_match.group(2)
            print(f"   ✅ FOUND KEY: {found_key[:10]}... (Hidden)")
        
        if wallet_match:
            found_wallet = wallet_match.group(2)
            print(f"   ✅ FOUND WALLET: {found_wallet}")

    # 3. Update Database if key is found
    if found_key:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        # Ensure Founder exists
        cur.execute("SELECT name FROM active_members WHERE user_id = 'FOUNDER-001'")
        if not cur.fetchone():
            cur.execute("INSERT INTO active_members (user_id, name, is_system_account) VALUES ('FOUNDER-001', 'THE FOUNDER', 1)")

        # Update
        if found_wallet:
            cur.execute("UPDATE active_members SET private_key = ?, wallet_address = ? WHERE user_id = 'FOUNDER-001'", (found_key, found_wallet))
        else:
            cur.execute("UPDATE active_members SET private_key = ? WHERE user_id = 'FOUNDER-001'", (found_key,))
            
        conn.commit()
        conn.close()
        print("-" * 50)
        print("   ✅ SUCCESS: Database updated with Key from secrets.py")
    else:
        print("   ❌ No Private Key pattern found in secrets.py")
        print("   Checking content manually...")
        print("-" * 50)
        # Show first few lines just in case (safe peek)
        print(content[:200]) 

if __name__ == "__main__":
    hunt_key()
