import psycopg2

def check_and_link_bloodline(child_name, father_name, mother_name):
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

        # Search for parents in the forbidden list
        cur.execute("SELECT id, full_name FROM the_forbidden_list WHERE full_name IN (%s, %s)", (father_name, mother_name))
        parent_match = cur.fetchone()

        if parent_match:
            parent_id = parent_match[0]
            parent_name = parent_match[1]
            print(f"⚠️ MATCH FOUND: {child_name} is linked to blocked parent {parent_name}.")
            
            # Auto-collect child's name into the forbidden list
            reason = f"Ancestral Block: Linked to parent {parent_name} (ID: {parent_id})"
            cur.execute("INSERT INTO the_forbidden_list (full_name, reason) VALUES (%s, %s)", (child_name, reason))
            
            conn.commit()
            print(f"🛡️  Bloodline Tracked: {child_name} has been added to the Forbidden List.")
            return True # Blocked
        
        return False # Clean
        
    except Exception as e:
        print(f"❌ Trace Error: {e}")
    finally:
        cur.close()
        conn.close()
