import psycopg2

def check_succession_eligibility(binary_id):
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

        # 1. Fetch User's Task Status
        cur.execute("""
            SELECT merchant_done, trading_done, engagement_done, downline_count 
            FROM portal_citizens WHERE binary_id = %s
        """, (binary_id,))
        user = cur.fetchone()

        if not user:
            return "ID not found."

        m_done, t_done, e_done, d_count = user
        
        # 2. Define the Perfect 20th Level Target
        PERFECT_20 = 1048576 

        print(f"--- Verification for ID {binary_id} ---")
        print(f"Merchant: {'✅' if m_done else '❌'}")
        print(f"Trading:  {'✅' if t_done else '❌'}")
        print(f"Engage:   {'✅' if e_done else '❌'}")
        print(f"Network:  {d_count}/{PERFECT_20} {'✅' if d_count >= PERFECT_20 else '❌'}")

        # 3. Master Trigger Logic
        if m_done and t_done and e_done and d_count >= PERFECT_20:
            print("\n🌟 STATUS: ALL SYSTEMS GREEN!")
            print("🚀 ACTION: 'EXIT TO PROJECT 2' BUTTON ENABLED.")
            
            # Update database to unlock the exit
            cur.execute("UPDATE portal_citizens SET can_exit = TRUE WHERE binary_id = %s", (binary_id,))
            conn.commit()
        else:
            print("\n⚠️ STATUS: SUCCESSION VERIFICATION REQUIRED.")
            print("Keep building and completing tasks to unlock the next project.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Logic Error: {e}")

if __name__ == "__main__":
    # Test for your current ID (386+)
    check_succession_eligibility(386)
