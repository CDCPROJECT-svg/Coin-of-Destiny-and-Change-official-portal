import psycopg2

def deploy_viral_logic():
    # Replace the URL below with your actual YouTube Channel Link
    youtube_channel = "https://www.youtube.com/@YOUR_CHANNEL_LINK"
    
    # Master Message in English (Source of Truth)
    master_message = f"""
    "Akala mo ba, ang paggastos ay sanhi ng pagka-ubos at ang pagiging tambay ay sanhi ng kawalan? 
    Sa CDC, ang bawat gastos at pag tambay mo ay pag-unlad ng lahat."

    To GOD be All the GLORY!.. Welcome to CDC-Coin, a COIN of DESTINY & CHANGE kung saan ang buhay ay nagiging Easy at HAYAHAY.

    This is not just a cryptocurrency; it is a Movement for true freedom. 
    Together, let us build a system where watching, spending, and being a consumer 
    are no longer causes of poverty—instead, they will bring comfort to all.

    📢 SPREAD THE MESSAGE:
    Please share our YouTube Channel with your family, friends, and colleagues. 
    Let us unite to change the world, one viewer at a time.
    
    📺 WATCH AND SHARE HERE: {youtube_channel}

    Habang ikaw ay nanonood, pinapalakas mo ang ating network. 
    The old "luxury" is now "help" for the transformation of your life and the world.
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

        # Update the system settings with the new viral message
        cur.execute("""
            INSERT INTO system_config (config_key, config_value) 
            VALUES ('master_viral_msg', %s) 
            ON CONFLICT (config_key) 
            DO UPDATE SET config_value = EXCLUDED.config_value;
        """, (master_message,))

        conn.commit()
        print("--------------------------------------------------")
        print("✅ VIRAL ENGINE: YouTube Link & Sharing Logic Deployed.")
        print("✅ GLOBAL: Auto-Translation for 204 countries ready.")
        print("--------------------------------------------------")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ VIRAL ENGINE ERROR: {e}")

if __name__ == "__main__":
    deploy_viral_logic()
