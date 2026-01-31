import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def inject_founder():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      💉 MANUAL KEY INJECTION (FLEXIBLE MODE)")
    print("=========================================================")
    print("   Please paste your Private Key starting with '0e...'")
    print("   The script will automatically format it correctly.")
    print("=========================================================")

    # 1. Ask for Input
    pkey = input("\n🔑 PASTE PRIVATE KEY HERE: ").strip()
    wallet = input("📬 PASTE WALLET ADDRESS HERE: ").strip()

    # 2. Auto-Fix Format
    # Kapag walang '0x', dagdagan natin sa unahan
    if not pkey.startswith("0x"):
        pkey = "0x" + pkey
        print(f"   ℹ️  Added '0x' prefix. Key is valid.")

    # 3. Update Database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        # Check Founder
        cur.execute("SELECT name FROM active_members WHERE user_id = 'FOUNDER-001'")
        if not cur.fetchone():
            cur.execute("INSERT INTO active_members (user_id, name, is_system_account) VALUES ('FOUNDER-001', 'THE FOUNDER', 1)")

        # Save
        cur.execute("""
            UPDATE active_members 
            SET private_key = ?, wallet_address = ? 
            WHERE user_id = 'FOUNDER-001'
        """, (pkey, wallet))
        
        conn.commit()
        print("\n" + "="*50)
        print("   ✅ SUCCESS! FOUNDER-001 credentials saved.")
        print("   Key stored successfully.")
        print("="*50)

    except Exception as e:
        print(f"\n❌ Error: {e}")

    conn.close()

if __name__ == "__main__":
    inject_founder()
