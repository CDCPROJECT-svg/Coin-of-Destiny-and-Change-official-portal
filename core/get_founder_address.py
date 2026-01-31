import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def get_founder():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get Founder-001 Address
    cursor.execute("SELECT user_id, wallet_address FROM active_members WHERE user_id = 'FOUNDER-001'")
    row = cursor.fetchone()
    
    if row:
        print("\n--- FOUNDER-001 WALLET (DEPLOYER) ---")
        print(f"User ID: {row[0]}")
        print(f"Address: {row[1]}")
        print("\nIMPORTANT: Please send at least 0.2 AMOY MATIC to this address.")
        print("This is needed for GAS FEE to deploy your Codac Coin.")
    else:
        print("Error: Founder account not found.")

    conn.close()

if __name__ == "__main__":
    get_founder()
