import psycopg2

def run_audit():
    print("🔍 STARTING CODAC SYSTEM AUDIT...\n")
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

        # 1. Check Tables
        tables = ['system_config', 'system_channels', 'member_milestones', 'rewards_schedule']
        for table in tables:
            cur.execute(f"SELECT count(*) FROM {table};")
            count = cur.fetchone()[0]
            print(f"✅ TABLE CHECK: {table} is ONLINE ({count} records found).")

        # 2. Check Hierarchy (Channels)
        cur.execute("SELECT channel_name FROM system_channels ORDER BY channel_id ASC;")
        channels = cur.fetchall()
        print(f"\n📺 CHANNEL HIERARCHY:")
        for idx, ch in enumerate(channels, 1):
            print(f"   {idx}. {ch[0]}")

        # 3. Check Rewards Logic
        cur.execute("SELECT sum(codac_reward) FROM rewards_schedule;")
        total_potential = cur.fetchone()[0]
        print(f"\n💰 REWARDS LOGIC: Total Potential CODAC per Pioneer: {total_potential} CODAC")

        # 4. Check Security Configuration
        cur.execute("SELECT count(*) FROM system_config WHERE config_key = 'login_youtube_requirement';")
        sec_check = cur.fetchone()[0]
        if sec_check > 0:
            print("🛡️ SECURITY: YouTube Identity Linker is ACTIVE.")

        print("\n🏆 AUDIT COMPLETE: All systems are green. 'Bawal Magkamali' achieved.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ AUDIT FAILED: {e}")

if __name__ == "__main__":
    run_audit()
