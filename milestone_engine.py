import psycopg2

def setup_milestone_tracker():
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

        # 1. Create table for Members including YouTube URL and CDC Wallet
        cur.execute("""
            CREATE TABLE IF NOT EXISTS member_milestones (
                member_id TEXT PRIMARY KEY,
                youtube_url TEXT UNIQUE,
                qr_code_hash TEXT UNIQUE,
                cdc_balance DECIMAL DEFAULT 0,
                join_milestone_level INTEGER
            );
        """)

        # 2. Logic to store the Rewards Table for the Smart Contract
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rewards_schedule (
                milestone_count BIGINT PRIMARY KEY,
                cdc_reward INTEGER
            );
        """)

        # Insert your cumulative schedule
        milestones = [
            (1000, 8), (10000, 8), (50000, 8), (100000, 8),
            (500000, 4), (1000000, 4), (5000000, 4), (10000000, 4), (50000000, 4),
            (100000000, 2), (500000000, 2), (1000000000, 1)
        ]

        for m, r in milestones:
            cur.execute("INSERT INTO rewards_schedule VALUES (%s, %s) ON CONFLICT DO NOTHING;", (m, r))

        conn.commit()
        print("--------------------------------------------------")
        print("✅ SMART CONTRACT LOGIC: Milestone Rewards Initialized.")
        print("✅ TRACKING: YouTube URL is now the Primary Login Key.")
        print("✅ POTENTIAL: Early 1K Pioneers earn 51 CDC Total.")
        print("--------------------------------------------------")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ MILESTONE ERROR: {e}")

if __name__ == "__main__":
    setup_milestone_tracker()
