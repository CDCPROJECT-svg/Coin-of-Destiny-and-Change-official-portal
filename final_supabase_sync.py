import psycopg2
import json

def sync_sovereign_logic():
    print("🚀 Initiating Master Sync to Supabase...")
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

        # 1. Update Level Requirements (Progressive Tasks)
        levels = []
        for i in range(1, 18):
            grand_bonus = 18888 + ((i-1) * 10000)
            merchant_req = grand_bonus * 0.02
            trading_req = 88 + ((i-1) * 100 if i > 1 else 0)
            engagement_pts = 188888 + ((i-1) * 100000)
            levels.append((i, engagement_pts, merchant_req, trading_req))

        cur.executemany("""
            INSERT INTO level_requirements (level_id, required_points, merchant_usd_req, trading_usd_req)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (level_id) DO UPDATE SET 
                required_points = EXCLUDED.required_points,
                merchant_usd_req = EXCLUDED.merchant_usd_req,
                trading_usd_req = EXCLUDED.trading_usd_req;
        """, levels)

        # 2. Update System Config for Splits & Withdrawals
        config_data = {
            "withdrawal_limit_pct": 0.08,
            "split_portal_treasury": 0.25,
            "split_portal_reserve": 0.25,
            "split_stakeholders": 0.125,
            "binary_exit_target": 1048576,
            "tax_disclaimer": "Member responsible for local country taxation."
        }
        
        cur.execute("""
            INSERT INTO system_config (config_key, config_value)
            VALUES ('sovereign_rules', %s)
            ON CONFLICT (config_key) DO UPDATE SET config_value = EXCLUDED.config_value;
        """, (json.dumps(config_data),))

        conn.commit()
        print("✅ SUCCESS: All tasks, splits, and binary targets are now LIVE on Supabase.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Sync Failed: {e}")

if __name__ == "__main__":
    sync_sovereign_logic()
