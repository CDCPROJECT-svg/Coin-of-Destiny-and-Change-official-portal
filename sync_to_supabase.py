import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def backup_code_to_db(filename):
    if not os.path.exists(filename):
        print(f"❌ File {filename} hindi nahanap.")
        return

    with open(filename, 'r') as file:
        code_content = file.read()

    try:
        conn = psycopg2.connect(
            dbname=os.getenv("SUPABASE_DB"),
            user=os.getenv("SUPABASE_USER"),
            password=os.getenv("SUPABASE_PASS"),
            host=os.getenv("SUPABASE_HOST"),
            port=os.getenv("SUPABASE_PORT"),
            sslmode="require"
        )

        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS code_backups (
            id SERIAL PRIMARY KEY,
            filename TEXT,
            content TEXT,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        cur.execute(
            "INSERT INTO code_backups (filename, content) VALUES (%s, %s);",
            (filename, code_content)
        )

        conn.commit()
        print(f"✅ SECURE BACKUP: {filename} saved safely.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Sync Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        backup_code_to_db(sys.argv[1])
    else:
        print("Usage: python3 sync_to_supabase.py filename")
