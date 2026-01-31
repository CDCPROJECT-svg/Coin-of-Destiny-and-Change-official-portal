import hashlib, psycopg2

def register_user(email, password):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
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
        
        # Registering only Email/Password first
        cur.execute("INSERT INTO citizens (email, password_hash, status) VALUES (%s, %s, %s)", 
                    (email, hashed_pw, 'WAITING_FOR_ID'))
        
        conn.commit()
        print(f"✅ Stage 1 Complete: {email} registered. Please verify email to proceed to Stage 2.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    email = input("Enter Email: ")
    pw = input("Enter Password: ")
    register_user(email, pw)
