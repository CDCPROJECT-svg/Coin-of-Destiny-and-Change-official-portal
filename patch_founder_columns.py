import psycopg2

def patch_database():
    print("🔧 Inaayos ang Founder Database Columns...")
    try:
        conn = psycopg2.connect(
            dbname='postgres', user='postgres.xzbozofttuvyijeimxkj',
            password='dnHmzMkSQhvMmCj8', host='aws-1-ap-south-1.pooler.supabase.com',
            port='6543', sslmode='require'
        )
        cur = conn.cursor()

        # 1. Idagdag ang mga kulang na columns sa portal_citizens
        cur.execute("""
            ALTER TABLE portal_citizens 
            ADD COLUMN IF NOT EXISTS reward_wallet NUMERIC DEFAULT 18888,
            ADD COLUMN IF NOT EXISTS codac_coin_wallet NUMERIC DEFAULT 0;
        """)

        # 2. Siguraduhin na may system_ledgers table para sa Treasury at Reserve
        cur.execute("""
            CREATE TABLE IF NOT EXISTS system_ledgers (
                id SERIAL PRIMARY KEY,
                treasury_balance NUMERIC DEFAULT 0,
                reserve_balance NUMERIC DEFAULT 0,
                last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 3. Maglagay ng initial record sa system_ledgers kung wala pa
        cur.execute("INSERT INTO system_ledgers (treasury_balance, reserve_balance) SELECT 0, 0 WHERE NOT EXISTS (SELECT 1 FROM system_ledgers);")

        conn.commit()
        print("✅ SUCCESS: Database Columns Patched! Handa na ang Founder View.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Patch Error: {e}")

if __name__ == "__main__":
    patch_database()
