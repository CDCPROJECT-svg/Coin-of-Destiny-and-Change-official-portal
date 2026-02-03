import psycopg2

def sync_wallet():
    print("🏛️ Synchronizing Master Founder Account (ID 386)...")
    try:
        conn = psycopg2.connect(
            dbname='postgres', user='postgres.xzbozofttuvyijeimxkj',
            password='dnHmzMkSQhvMmCj8', host='aws-1-ap-south-1.pooler.supabase.com',
            port='6543', sslmode='require'
        )
        cur = conn.cursor()

        # 1. I-check kung nandoon na ang ID 386
        cur.execute("SELECT binary_id FROM portal_citizens WHERE binary_id = 386;")
        exists = cur.fetchone()

        if not exists:
            # Kung wala pa, i-insert gamit ang tamang columns
            print("✨ Creating Master Record...")
            cur.execute("""
                INSERT INTO portal_citizens 
                (binary_id, full_name, status, project_id, reward_wallet, codac_coin_wallet) 
                VALUES (386, 'MASTER FOUNDER', 'ACTIVE', 1, 18888, 0);
            """)
        else:
            # Kung nandoon na, i-update lang ang balanse (SAFE: Hindi gagalawin ang password_hash)
            print("🔄 Updating Wallet Balance for existing ID 386...")
            cur.execute("""
                UPDATE portal_citizens 
                SET reward_wallet = 18888, 
                    full_name = 'MASTER FOUNDER',
                    status = 'ACTIVE'
                WHERE binary_id = 386;
            """)

        conn.commit()
        print("✅ SUCCESS: Master Founder Account is now Synced and Secured.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    sync_wallet()
