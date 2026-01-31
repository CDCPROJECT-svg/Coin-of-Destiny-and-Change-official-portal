import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def reset_to_zero():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("   [SYSTEM] Resetting System Wallets to 0.00 (Transparency Protocol)...")

    # Listahan ng System Wallets na gagawing Zero
    system_wallets = [
        "TREASURY-001",
        "INCENTIVE-001",
        "INFRA-001",
        "FOUNDATION-001",
        "COUNTRY-PH",
        "FORFEITED-001"
    ]

    for uid in system_wallets:
        cur.execute("UPDATE active_members SET trading_points = 0.00 WHERE user_id = ?", (uid,))
        print(f"   ✅ {uid} balance set to 0.00")

    conn.commit()
    conn.close()
    print("\n   [SUCCESS] All Portal Wallets are now Clean/Zero.")

if __name__ == "__main__":
    reset_to_zero()
