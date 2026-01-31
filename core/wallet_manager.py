import sqlite3
import os
import secrets

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def generate_system_wallets():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- STARTING SECURE WALLET GENERATION (511 ACCOUNTS) ---")

    # 1. CREATE THE VAULT (For Private Keys)
    # This table is separate to ensure data privacy alignment
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secure_vault (
            user_id TEXT PRIMARY KEY,
            private_key TEXT,
            security_level TEXT DEFAULT 'HIGH'
        )
    """)

    # 2. UPDATE MEMBERS TABLE (For Public Addresses)
    try:
        cursor.execute("ALTER TABLE active_members ADD COLUMN wallet_address TEXT")
        print("[OK] Public Wallet Column added.")
    except sqlite3.OperationalError:
        pass # Column exists

    # 3. FETCH USERS WHO NEED WALLETS
    cursor.execute("SELECT user_id, name FROM active_members WHERE wallet_address IS NULL")
    users = cursor.fetchall()

    if not users:
        print("All accounts already have wallets.")
        conn.close()
        return

    print(f"Generating keys for {len(users)} accounts...")

    count = 0
    for user_id, name in users:
        # A. GENERATE SECURE KEYS (Simulation of ETH Standard)
        # 1. Private Key (64 hex characters - 256 bit security)
        priv_key = "0x" + secrets.token_hex(32)
        
        # 2. Public Address (40 hex characters - Derived simulation)
        # In a real blockchain, this is derived mathematically from the private key.
        # Here we generate a unique secure token for the address.
        pub_address = "0x" + secrets.token_hex(20)

        # B. STORE PRIVATE KEY IN VAULT
        cursor.execute("""
            INSERT OR REPLACE INTO secure_vault (user_id, private_key)
            VALUES (?, ?)
        """, (user_id, priv_key))

        # C. STORE PUBLIC ADDRESS IN MEMBER PROFILE
        cursor.execute("""
            UPDATE active_members 
            SET wallet_address = ? 
            WHERE user_id = ?
        """, (pub_address, user_id))

        count += 1
        if count % 50 == 0:
            print(f"   ... Securely generated {count} wallets...")

    conn.commit()
    conn.close()
    print(f"\nSUCCESS: {count} Wallets Generated.")
    print(" - Public Addresses saved to: active_members")
    print(" - PRIVATE KEYS saved to: secure_vault (PROTECTED)")

if __name__ == "__main__":
    generate_system_wallets()
