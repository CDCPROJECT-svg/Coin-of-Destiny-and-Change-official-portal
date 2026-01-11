import psycopg2

def cleanup():
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

        # 1. Burahin ang maling entry
        cur.execute("DELETE FROM system_channels;")
        
        # 2. Ipasok ang tamang entry
        correct_name = "CDC MAIN CHANNEL"
        correct_url = "https://youtube.com/@catalystdynamocreature8?si=GSm4m6B6j-A5TlYi"
        
        cur.execute("""
            INSERT INTO system_channels (channel_name, channel_url) 
            VALUES (%s, %s);
        """, (correct_name, correct_url))

        conn.commit()
        print("--------------------------------------------------")
        print("✅ DATABASE CLEANED: Entry has been corrected.")
        print(f"✅ NAME: {correct_name}")
        print(f"✅ URL: {correct_url}")
        print("--------------------------------------------------")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

if __name__ == "__main__":
    cleanup()
