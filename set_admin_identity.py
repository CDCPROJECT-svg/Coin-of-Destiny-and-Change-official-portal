import psycopg2

def lock_founder_identity():
    print("👑 Setting Master Founder Identity for ID 386...")
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

        # Update ID 386 with Master Privileges
        cur.execute("""
            UPDATE portal_citizens 
            SET username = 'MASTER FOUNDER', 
                role = 'ADMIN',
                can_exit = TRUE 
            WHERE binary_id = 386;
        """)

        conn.commit()
        print("✅ Identity Locked: ID 386 is now recognized as the MASTER FOUNDER.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Identity Error: {e}")

if __name__ == "__main__":
    lock_founder_identity()
