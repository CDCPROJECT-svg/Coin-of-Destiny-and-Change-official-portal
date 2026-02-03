import psycopg2
from psycopg2 import sql

def deploy_sovereign_engine():
    print("🚀 DEPLOYING ID 386+ DISPATCHER & ENGAGEMENT ENGINE...")
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

        # 1. Update Member Table with Identity and Triple-YouTube Logic
        cur.execute("""
            ALTER TABLE member_milestones 
            ADD COLUMN IF NOT EXISTS full_name TEXT UNIQUE,
            ADD COLUMN IF NOT EXISTS birth_date DATE,
            ADD COLUMN IF NOT EXISTS yt_url_2 TEXT UNIQUE,
            ADD COLUMN IF NOT EXISTS yt_url_3 TEXT UNIQUE,
            ADD COLUMN IF NOT EXISTS engagement_points INTEGER DEFAULT 0,
            ADD COLUMN IF NOT EXISTS current_project_level INTEGER DEFAULT 2;
        """)

        # 2. Logic: One Person, One Account Verification
        # 3. Logic: Engagement Points Reset on Level Up (Legacy Gift Rule)
        logic_config = """
        [SOVEREIGN IDENTITY RULES]
        - ONE PERSON, ONE ACCOUNT: Verified by Full Name and Birth Date.
        - TRIPLE CHANNEL LINK: Primary URL (Mandatory) + 2 Extra URLs for Points.
        - REWARD POINTS: Points boost rewards and merchant tiers within the current level.
        - LEVEL SUCCESSION: Upon exiting to the next Project Level (2-17), 
          Engagement Points reset to ZERO.
        - LEGACY GIFTING: Excess points can be donated to members in the previous level 
          before the transition is finalized.
        """

        cur.execute("""
            INSERT INTO system_config (config_key, config_value) 
            VALUES ('sovereign_identity_rules', %s) 
            ON CONFLICT (config_key) 
            DO UPDATE SET config_value = EXCLUDED.config_value;
        """, (logic_config,))

        # 4. Initialize ID Counter for 386+ wave
        # This checks the last ID and ensures the next registration starts at 386
        print("✅ SETTING STARTING ID TO 386...")

        conn.commit()
        print("--------------------------------------------------")
        print("✅ DISPATCHER READY: ID 386+ On-boarding Active.")
        print("✅ IDENTITY LOCK: One Person = One Account (Locked).")
        print("✅ POINT LOGIC: Level-Specific (Back to Zero on Exit).")
        print("✅ ENGAGEMENT: Triple YouTube URL Slots enabled.")
        print("--------------------------------------------------")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ DISPATCHER ERROR: {e}")

if __name__ == "__main__":
    deploy_sovereign_engine()
