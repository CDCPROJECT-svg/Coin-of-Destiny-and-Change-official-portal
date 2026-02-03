import psycopg2
import hashlib

def update_admin_password(new_password):
    # Dito ginagawa ang 'hashing' para maging secure
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    
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

        # Ang hashed_password ang ise-save, hindi ang mismong text
        cur.execute("""
            UPDATE portal_citizens 
            SET password_hash = %s 
            WHERE binary_id = 386;
        """, (hashed_password,))

        conn.commit()
        print("\n✅ SUCCESS: Ang password para sa ID 386 ay na-update na!")
        print("🛡️ Naka-encrypt na ito sa database (SHA-256).")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # DITO MO ILALAGAY ANG PASSWORD MO:
      update_admin_password('Uday_1976Cdbudz112802')
