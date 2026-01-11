import os
import psycopg2

SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

def seed_database():
    try:
        conn = psycopg2.connect(SUPABASE_DB_URL)
        cur = conn.cursor()
        
        # 1. Create the table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                project_id INTEGER DEFAULT 1,
                leadership_title TEXT DEFAULT 'Ambassador'
            );
        """)
        
        # 2. Insert the Founder (ID 1)
        cur.execute("""
            INSERT INTO members (id, project_id, leadership_title)
            VALUES (1, 1, 'Ambassador')
            ON CONFLICT (id) DO NOTHING;
        """)
        
        # 3. Add a test member for the binary tree (ID 500)
        cur.execute("""
            INSERT INTO members (id, project_id, leadership_title)
            VALUES (500, 2, 'Captain')
            ON CONFLICT (id) DO NOTHING;
        """)
        
        conn.commit()
        print("✅ Global Registry Populated Successfully!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Seed Error: {e}")

if __name__ == "__main__":
    seed_database()
