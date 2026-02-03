import psycopg2

def select_incentive(binary_id, choice):
    options = {1:"CAR", 2:"SHOPPING", 3:"TRAVEL", 4:"HEALTH", 5:"EDUCATION", 6:"HOME"}
    if choice not in options: return "Invalid"
    
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres.xzbozofttuvyijeimxkj', password='dnHmzMkSQhvMmCj8', host='aws-1-ap-south-1.pooler.supabase.com', port='6543', sslmode='require')
        cur = conn.cursor()
        
        # Lock the 7,777 Incentive and set to Cycle B
        cur.execute("""
            UPDATE portal_citizens 
            SET incentive_category = %s, incentive_balance = 17777, has_selected_incentive = TRUE 
            WHERE binary_id = %s AND has_selected_incentive = FALSE
        """, (options[choice], binary_id))
        
        conn.commit()
        print(f"✅ Choice {options[choice]} locked for ID {binary_id}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    select_incentive(1, 1) # Test for Founder
