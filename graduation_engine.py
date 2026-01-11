import psycopg2

def graduate_to_cycle_2(binary_id):
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

        # 1. Verify if the account is in Level 18
        cur.execute("SELECT entry_level, cdc_points_balance, is_elite FROM portal_citizens WHERE binary_id = %s", (binary_id,))
        level, balance, is_elite = cur.fetchone()

        if level == 18 and is_elite:
            print(f"🎓 ID {binary_id} is graduating Level 18. Carrying over {balance} points.")
            
            # 2. Update status for Cycle 2 and keep the balance
            # Cycle 'A' becomes Cycle 'B'
            cur.execute("""
                UPDATE portal_citizens 
                SET cycle_code = 'B', 
                    entry_level = 1, 
                    status = 're-entered'
                WHERE binary_id = %s
            """, (binary_id,))
            
            # Note: Because we DON'T reset balance here, the points are "carried over."
            
        else:
            # If they exit level 1-17, points are burned (back to zero)
            cur.execute("UPDATE portal_citizens SET cdc_points_balance = 0 WHERE binary_id = %s", (binary_id,))
            print(f"🔥 ID {binary_id} exited Level {level}. Points burned.")

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Graduation Error: {e}")

if __name__ == "__main__":
    # Test for ID 1 (Founder)
    graduate_to_cycle_2(1)
