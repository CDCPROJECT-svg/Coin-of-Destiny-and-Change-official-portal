import psycopg2
import json

def audit_state():
    try:
        conn = psycopg2.connect(
            dbname='postgres', user='postgres.xzbozofttuvyijeimxkj',
            password='dnHmzMkSQhvMmCj8', host='aws-1-ap-south-1.pooler.supabase.com',
            port='6543', sslmode='require'
        )
        cur = conn.cursor()
        cur.execute("SELECT config_key, config_value FROM system_config WHERE config_key IN ('sovereign_rules', 'sovereign_state');")
        rows = cur.fetchall()
        
        print("\n--- CODAC SYSTEM PROTECTION AUDIT ---")
        for row in rows:
            print(f"STATUS [{row[0]}]: {row[1]}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    audit_state()
