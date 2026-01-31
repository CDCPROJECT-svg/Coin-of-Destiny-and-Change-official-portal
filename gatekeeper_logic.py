import psycopg2

def deploy_gatekeeper():
    gatekeeper_message = """
    🛡️ CODAC PORTAL SECURITY:
    Access to the Portal (Sign-up/Login) is EXCLUSIVELY granted to SUBSCRIBERS.
    
    1. Primary Key: Subscribe to Catalyst Dynamo Creature.
    2. Support Key: Subscribe to The Malakat.
    
    NOTE: Likes, Shares, and Notifications help spread the message to others, 
    but only a VALID SUBSCRIPTION triggers your official on-boarding to the 
    CODAC Coin of Destiny & Change Portal.
    """

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

        # Update the gateway policy
        cur.execute("""
            INSERT INTO system_config (config_key, config_value) 
            VALUES ('onboarding_trigger_policy', %s) 
            ON CONFLICT (config_key) 
            DO UPDATE SET config_value = EXCLUDED.config_value;
        """, (gatekeeper_message,))

        conn.commit()
        print("--------------------------------------------------")
        print("✅ GATEKEEPER UPDATED: Subscription is the only trigger.")
        print("✅ LOGIC: Like/Share/Bell = Engagement (Non-Trigger).")
        print("✅ LOGIC: Subscribed = Authorized to Sign-Up/Login.")
        print("--------------------------------------------------")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ GATEKEEPER ERROR: {e}")

if __name__ == "__main__":
    deploy_gatekeeper()
