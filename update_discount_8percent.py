import psycopg2

def update_to_eight_percent():
    print("🏪 UPDATING MERCHANT DISCOUNT POLICY (MIN 8%)...")
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

        # Update the default discount rate to 8%
        cur.execute("ALTER TABLE merchant_registry ALTER COLUMN discount_rate SET DEFAULT 8;")
        
        # Update the logic message for the scanner
        validation_script = """
        [CDC MERCHANT VALIDATION]
        1. SCAN Member Passport QR.
        2. VERIFY CDC Portal Membership.
        3. APPLY MANDATORY MINIMUM 8% DISCOUNT.
        4. ADDITIONAL: Merchants may offer more (Additional Pa-More) 
           at their own discretion based on business capacity.
        """

        cur.execute("""
            INSERT INTO system_config (config_key, config_value) 
            VALUES ('merchant_validation_logic', %s) 
            ON CONFLICT (config_key) 
            DO UPDATE SET config_value = EXCLUDED.config_value;
        """, (validation_script,))

        conn.commit()
        print("--------------------------------------------------")
        print("✅ POLICY UPDATED: Minimum 8% Discount Standard.")
        print("✅ SYMBOLISM: 8% Discount matches the 8 CDC Milestone Reward.")
        print("✅ FLEXIBILITY: 'Additional Pa-more' is still active.")
        print("--------------------------------------------------")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ POLICY UPDATE ERROR: {e}")

if __name__ == "__main__":
    update_to_eight_percent()
