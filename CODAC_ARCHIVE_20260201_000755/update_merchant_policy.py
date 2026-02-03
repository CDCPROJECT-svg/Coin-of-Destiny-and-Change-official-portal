import psycopg2

def update_policy():
    print("🏪 UPDATING MERCHANT DISCOUNT POLICY (MIN 10%)...")
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

        # Update the default discount rate in the registry to 10%
        cur.execute("ALTER TABLE merchant_registry ALTER COLUMN discount_rate SET DEFAULT 10;")
        
        # Update the logic message for the scanner
        validation_script = """
        [CODAC MERCHANT VALIDATION]
        1. SCAN Member Passport QR.
        2. VERIFY CODAC Portal Membership.
        3. APPLY MANDATORY MINIMUM 10% DISCOUNT.
        4. ADDITIONAL: Merchants may offer more (Additional Pa-More) 
           at their own discretion.
        """

        cur.execute("""
            INSERT INTO system_config (config_key, config_value) 
            VALUES ('merchant_validation_logic', %s) 
            ON CONFLICT (config_key) 
            DO UPDATE SET config_value = EXCLUDED.config_value;
        """, (validation_script,))

        conn.commit()
        print("--------------------------------------------------")
        print("✅ POLICY UPDATED: Minimum 10% Discount Standard.")
        print("✅ FLEXIBILITY: Merchants can now offer 'Additional Pa-more'.")
        print("✅ PROJECT SYNC: Ready for Projects 2-18 merchants.")
        print("--------------------------------------------------")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ POLICY UPDATE ERROR: {e}")

if __name__ == "__main__":
    update_policy()
