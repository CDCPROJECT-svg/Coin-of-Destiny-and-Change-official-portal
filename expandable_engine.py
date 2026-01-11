import psycopg2

def setup_expansion():
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

        # 1. Create Table for YouTube Channels (Ready for 3+ channels)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS system_channels (
                channel_id SERIAL PRIMARY KEY,
                channel_name TEXT,
                channel_url TEXT,
                is_active BOOLEAN DEFAULT TRUE
            );
        """)

        # 2. Add your Main Channel (Placeholder - You can add more easily)
        # To add more, just add more lines like the one below
        cur.execute("""
            INSERT INTO system_channels (channel_name, channel_url) 
            VALUES ('CDC Main Channel', 'https://www.youtube.com/@CDC_OFFICIAL')
            ON CONFLICT DO NOTHING;
        """)

        # 3. Create Table for Founders/Leadership
        cur.execute("""
            CREATE TABLE IF NOT EXISTS leadership_registry (
                role_title TEXT PRIMARY KEY,
                name TEXT,
                designed_id TEXT
            );
        """)

        # Set the Main Founder (ID 1)
        cur.execute("""
            INSERT INTO leadership_registry (role_title, name, designed_id) 
            VALUES ('Main Founder', 'Founder', 'CDC-A01L-GLB-000-000-001')
            ON CONFLICT (role_title) DO UPDATE SET name = EXCLUDED.name;
        """)

        conn.commit()
        print("--------------------------------------------------")
        print("✅ SCALABILITY: Multi-Channel & Founder Tables Ready.")
        print("✅ FUTURE-PROOF: You can now add 3 or more channels.")
        print("--------------------------------------------------")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ SETUP ERROR: {e}")

if __name__ == "__main__":
    setup_expansion()
