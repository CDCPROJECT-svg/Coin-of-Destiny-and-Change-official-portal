import sqlite3
import os
import secrets
from ecdsa import SECP256k1, SigningKey
from Crypto.Hash import keccak

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def generate_real_evm_wallets():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- GENERATING REAL EVM WALLETS (LIGHTWEIGHT METHOD) ---")

    # FIX: Create the VAULT table first if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secure_vault (
            user_id TEXT PRIMARY KEY,
            private_key TEXT,
            security_level TEXT DEFAULT 'HIGH'
        )
    """)
    
    # Ensure wallet_address column exists
    try:
        cursor.execute("ALTER TABLE active_members ADD COLUMN wallet_address TEXT")
    except sqlite3.OperationalError:
        pass 

    print("Vault initialized. Creating mathematically valid keys for Polygon Amoy...")

    # Fetch users
    cursor.execute("SELECT user_id, name FROM active_members")
    users = cursor.fetchall()
    
    total_users = len(users)
    print(f"Target: {total_users} Accounts.")

    # Helper for address checksum
    def to_checksum_address(address):
        address = address.lower().replace('0x', '')
        k = keccak.new(digest_bits=256)
        k.update(address.encode('utf-8'))
        hash_hex = k.hexdigest()
        checksum = "0x"
        for i, char in enumerate(address):
            if int(hash_hex[i], 16) >= 8:
                checksum += char.upper()
            else:
                checksum += char
        return checksum

    count = 0
    for user_id, name in users:
        # A. Generate Private Key
        priv_bytes = secrets.token_bytes(32)
        priv_hex = "0x" + priv_bytes.hex()

        # B. Derive Public Key
        sk = SigningKey.from_string(priv_bytes, curve=SECP256k1)
        pub_key = sk.verifying_key.to_string()

        # C. Derive Address
        k = keccak.new(digest_bits=256)
        k.update(pub_key)
        raw_address = k.hexdigest()[-40:]
        final_address = to_checksum_address(raw_address)

        # D. Save Data
        cursor.execute("INSERT OR REPLACE INTO secure_vault (user_id, private_key) VALUES (?, ?)", (user_id, priv_hex))
        cursor.execute("UPDATE active_members SET wallet_address = ? WHERE user_id = ?", (final_address, user_id))

        count += 1
        if count % 50 == 0:
            print(f"   ... Generated {count} Wallets...")

    conn.commit()
    conn.close()
    print(f"\nSUCCESS: {count} Real EVM Wallets Generated.")

if __name__ == "__main__":
    generate_real_evm_wallets()
