import psycopg2

def organize_db():
    print("🔧 Ine-organisa ang iyong 18 Projects sa database...")
    try:
        conn = psycopg2.connect(
            dbname='postgres', user='postgres.xzbozofttuvyijeimxkj',
            password='dnHmzMkSQhvMmCj8', host='aws-1-ap-south-1.pooler.supabase.com',
            port='6543', sslmode='require'
        )
        cur = conn.cursor()

        # 1. Idagdag ang project_id column (Default is 1 para sa Project 1)
        cur.execute("ALTER TABLE portal_citizens ADD COLUMN IF NOT EXISTS project_id INTEGER DEFAULT 1;")
        
        # 2. I-update ang lahat ng existing records para maging Project 1
        cur.execute("UPDATE portal_citizens SET project_id = 1 WHERE project_id IS NULL;")

        conn.commit()
        print("✅ SUCCESS: Ang Project Classification ay active na!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    organize_db()
