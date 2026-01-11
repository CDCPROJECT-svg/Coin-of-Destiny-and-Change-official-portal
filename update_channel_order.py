import psycopg2

def update_hierarchy():
    main_channel = "https://youtube.com/@catalystdynamocreature8?si=GSm4m6B6j-A5TlYi"
    secondary_channel = "https://youtube.com/@themalakat?si=0uL5q74M_Z9tD_va"
    
    onboarding_text = f"""
    "Akala mo ba, ang paggastos ay sanhi ng pagka-ubos at ang pagiging tambay ay sanhi ng kawalan? 
    Sa CDC, ang bawat gastos at pag tambay mo ay pag-unlad ng lahat."

    To GOD be All the GLORY!.. Welcome to CDC-Coin, a COIN of DESTINY & CHANGE.

    📢 OFFICIAL ON-BOARDING INSTRUCTIONS:
    
    STEP 1: Subscribe to our MAIN CHANNEL
    🔗 {main_channel}
    
    STEP 2: Subscribe to our SUPPORT CHANNEL
    🔗 {secondary_channel}

    🔔 IMPORTANT: 
    CLICK ALL NOTIFICATIONS on both channels to on-board CDC-Coin of Destiny & Change Portal 
    where life becomes Easy and HAYAHAY.

    Once you have completed these steps, you will receive your exclusive access 
    link to the portal.
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

        # Update the master message
        cur.execute("""
            INSERT INTO system_config (config_key, config_value) 
            VALUES ('master_viral_msg', %s) 
            ON CONFLICT (config_key) 
            DO UPDATE SET config_value = EXCLUDED.config_value;
        """, (onboarding_text,))

        conn.commit()
        print("--------------------------------------------------")
        print("✅ HIERARCHY UPDATED: Main Channel is now at the TOP.")
        print("✅ CHANNEL 1: Catalyst Dynamo Creature")
        print("✅ CHANNEL 2: The Malakat")
        print("--------------------------------------------------")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ UPDATE ERROR: {e}")

if __name__ == "__main__":
    update_hierarchy()
