import psycopg2

def setup_merchant_validator():
    print("🏪 DEPLOYING MERCHANT DISCOUNT VALIDATOR (8% MINIMUM)...")
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

        # 1. Ensure Merchant Registry exists with 8% Default
        cur.execute("""
            CREATE TABLE IF NOT EXISTS merchant_registry (
                merchant_id SERIAL PRIMARY KEY,
                merchant_name TEXT UNIQUE,
                merchant_category TEXT,
                discount_rate INTEGER DEFAULT 8,
                status TEXT DEFAULT 'ACTIVE'
            );
        """)

        # 2. Finalize the 8% + 'Pa-More' Logic
        validation_script = """
        [CODAC MERCHANT VALIDATION]
        1. SCAN Member Passport QR.
        2. VERIFY CODAC Portal Membership & Wallet Link.
        3. APPLY MANDATORY MINIMUM 8% DISCOUNT.
        4. ADDITIONAL: Merchants may provide 'Additional Pa-More' 
           discounts at their discretion.
        """

        cur.execute("""
            INSERT INTO system_config (config_key, config_value) 
            VALUES ('merchant_validation_logic', %s) 
            ON CONFLICT (config_key) 
            DO UPDATE SET config_value = EXCLUDED.config_value;
        """, (validation_script,))

        conn.commit()
        print("--------------------------------------------------")
        print("✅ MERCHANT STACK: 8% Minimum Standard Deployed.")
        print("✅ SYSTEM: Ready for Projects 2-18 Merchant Scan.")
        print("--------------------------------------------------")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ MERCHANT SETUP ERROR: {e}")

if __name__ == "__main__":
    setup_merchant_validator()
