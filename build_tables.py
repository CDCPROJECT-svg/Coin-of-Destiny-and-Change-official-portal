import psycopg2

def build_everything():
    print("🛠️  BUILDING SOVEREIGN DATABASE TABLES...")
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

        # 1. Create system_config table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS system_config (
                config_key TEXT PRIMARY KEY,
                config_value TEXT
            );
        """)
        
        # 2. Create system_channels table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS system_channels (
                channel_id SERIAL PRIMARY KEY,
                channel_name TEXT,
                channel_url TEXT
            );
        """)

        # 3. Create rewards_schedule table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rewards_schedule (
                milestone_count BIGINT PRIMARY KEY,
                codac_reward INTEGER
            );
        """)

        # 4. Create member_milestones table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS member_milestones (
                member_id TEXT PRIMARY KEY,
                youtube_url TEXT UNIQUE,
                codac_balance DECIMAL DEFAULT 0
            );
        """)

        conn.commit()
        print("✅ SUCCESS: All tables created and connected.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ BUILD ERROR: {e}")

if __name__ == "__main__":
    build_everything()
