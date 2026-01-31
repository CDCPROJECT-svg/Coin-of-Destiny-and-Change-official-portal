import os
import psycopg2

def connect():
    try:
        conn = psycopg2.connect(os.getenv("SUPABASE_DB_URL"))
        cur = conn.cursor()
        
        # Insert Founder (ID 1) into Project 1 (28 Levels)
        # We set 'current_level' to 20 to test the Exit Logic
        cur.execute("""
            INSERT INTO codac_users (id, project_id, current_level, leadership_status)
            VALUES (1, 1, 20, 'AMBASSADOR')
            ON CONFLICT (id) DO UPDATE SET current_level = 20;
        """)
        
        conn.commit()
        print("✅ Global Tree Initialized: Member 1 is now at Level 20.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    connect()
