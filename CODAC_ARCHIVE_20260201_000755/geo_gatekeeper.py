import psycopg2

# List of "Safe" countries (Tier 1)
SAFE_COUNTRIES = ['AU', 'PH', 'NZ', 'SG'] # Victoria/Melbourne (AU) is safe.

def apply_geographical_shield(user_country, user_id):
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

        if user_country not in SAFE_COUNTRIES:
            # Force into Holding Tank for Manual Founder Review
            cur.execute("UPDATE citizens SET status = 'HOLDING_TANK_MANUAL' WHERE id = %s", (user_id,))
            conn.commit()
            print(f"⚠️ SECURITY ALERT: User {user_id} from {user_country} moved to Holding Tank.")
            return "MANUAL_REVIEW_REQUIRED"
        
        return "PROCEED_TO_IDENTITY_FORM"

    except Exception as e:
        print(f"❌ Geo-Shield Error: {e}")
    finally:
        cur.close()
        conn.close()
