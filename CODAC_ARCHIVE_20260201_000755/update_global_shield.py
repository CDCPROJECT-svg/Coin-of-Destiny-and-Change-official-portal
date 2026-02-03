import psycopg2

def add_global_shield():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres.xzbozofttuvyijeimxkj',
            password='dnHmzMkSQhvMmCj8',
            host='aws-1-ap-south-1.pooler.supabase.com',
            port='6543',
            sslmode='require'
        )
        cur = conn.cursor()

        # Adding columns for foreign security
        cur.execute("""
            ALTER TABLE the_forbidden_list 
            ADD COLUMN IF NOT EXISTS country_code TEXT,
            ADD COLUMN IF NOT EXISTS ip_address TEXT,
            ADD COLUMN IF NOT EXISTS device_fingerprint TEXT;
        """)

        conn.commit()
        print("✅ GLOBAL SHIELD: Country and IP tracking added to Forbidden List.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Shield Error: {e}")

if __name__ == "__main__":
    add_global_shield()
