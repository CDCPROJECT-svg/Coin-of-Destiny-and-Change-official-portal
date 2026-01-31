import psycopg2

def upgrade_to_global():
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

        # Adding Country Tracking for all 204 nations
        cur.execute("""
            ALTER TABLE citizens 
            ADD COLUMN IF NOT EXISTS country_name TEXT,
            ADD COLUMN IF NOT EXISTS ip_proxy_detected BOOLEAN DEFAULT FALSE;
        """)

        conn.commit()
        print("✅ GLOBAL REGISTRY: Support for 204 countries is now ACTIVE.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Global Upgrade Error: {e}")

if __name__ == "__main__":
    upgrade_to_global()
