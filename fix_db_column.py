import psycopg2

def add_password_column():
    print("🔧 Ine-expand ang database structure para sa security...")
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

        # Idagdag ang password_hash column
        cur.execute("ALTER TABLE portal_citizens ADD COLUMN IF NOT EXISTS password_hash TEXT;")
        
        conn.commit()
        print("✅ SUCCESS: Ang 'password_hash' column ay naidagdag na sa Supabase!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error sa pag-update ng DB: {e}")

if __name__ == "__main__":
    add_password_column()
