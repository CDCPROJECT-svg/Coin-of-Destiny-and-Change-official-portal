import psycopg2

def enforce_no_bypass(user_id):
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
        
        # Fetch current status of the user
        cur.execute("SELECT status FROM citizens WHERE id = %s", (user_id,))
        status = cur.fetchone()[0]
        
        if status == 'WAITING_FOR_ID':
            return {
                "access": "DENIED",
                "redirect": "identity_vault_form",
                "message": "MANDATORY: Submit Father/Mother names and ID to unlock Portal."
            }
        
        elif status == 'ANCESTRAL_BLOCKED':
            return {
                "access": "PERMANENT_DENIAL",
                "redirect": "blocked_screen",
                "message": "ACCESS RESTRICTED: Ancestral Block Active."
            }
            
        elif status == 'PENDING_REVIEW':
            return {
                "access": "RESTRICTED",
                "redirect": "dimmed_dashboard",
                "message": "Under Review. Projects 2-18 are currently dimmed."
            }

        return {"access": "GRANTED", "redirect": "full_dashboard"}

    except Exception as e:
        print(f"Error in Gatekeeper: {e}")
    finally:
        cur.close()
        conn.close()
