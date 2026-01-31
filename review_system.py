import psycopg2

def review_admin_status():
    print("\n--- 🛡️ CODAC SOVEREIGN SYSTEM AUDIT ---")
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

        # I-check ang details ng ID 386
        cur.execute("""
            SELECT binary_id, username, role, 
                   (password_hash IS NOT NULL) as has_password,
                   SUBSTRING(password_hash, 1, 10) || '...' as hash_preview
            FROM portal_citizens 
            WHERE binary_id = 386;
        """)
        row = cur.fetchone()

        if row:
            print(f"📍 Binary ID     : {row[0]}")
            print(f"👤 Username      : {row[1]}")
            print(f"🎖️ Role          : {row[2]}")
            print(f"🔒 Password Set? : {'YES ✅' if row[3] else 'NO ❌'}")
            print(f"🔑 Hash Preview  : {row[4]} (Encrypted for your safety)")
        else:
            print("❌ Error: ID 386 not found in the database.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    review_admin_status()
