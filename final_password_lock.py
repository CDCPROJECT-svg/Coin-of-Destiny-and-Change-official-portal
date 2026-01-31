import psycopg2
import hashlib

def lock_password():
    # Ang iyong password ay Dikoalamvirus
    plain_text_pass = 'Uday_1976Cdbudz112802'
    hashed_pass = hashlib.sha256(plain_text_pass.encode()).hexdigest()
    
    print("🛡️ Siniselyuhan ang Master Founder Password...")
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

        # I-update na natin ang ID 386 gamit ang bagong column
        cur.execute("""
            UPDATE portal_citizens 
            SET password_hash = %s 
            WHERE binary_id = 386;
        """, (hashed_pass,))

        conn.commit()
        print("\n✅ KEY LOCKED: Ang ID 386 ay protektado na ng iyong password.")
        print("📍 Maaari mo na itong gamitin sa iyong Online Login.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    lock_password()
