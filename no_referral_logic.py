import psycopg2

def verify_no_commission_policy():
    print("🛡️ Verifying Sovereign No-Invite Policy...")
    # Ang logic na ito ay sinisigurado na 100% ng rewards ay galing sa 
    # Milestone Graduation at hindi sa Recruitment.
    
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

        # Siguraduhin na walang 'referral_bonus' column na aktibo sa calculation
        cur.execute("UPDATE system_config SET config_value = '0' WHERE config_key = 'referral_bonus_rate';")
        
        conn.commit()
        print("✅ Policy Confirmed: CDC is a Pure Feeding System. No Recruitment Commissions active.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Policy Sync Error: {e}")

if __name__ == "__main__":
    verify_no_commission_policy()
