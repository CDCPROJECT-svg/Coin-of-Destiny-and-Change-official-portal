import psycopg2

def gift_engagement_points(from_binary_id, to_binary_id, points_to_gift):
    """
    In CDC, we don't give referral money. 
    We gift 'Engagement Points' to help downlines graduate faster.
    """
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

        # 1. Check if the Giver has enough points
        cur.execute("SELECT engagement_points FROM portal_citizens WHERE binary_id = %s", (from_binary_id,))
        giver_points = cur.fetchone()[0]

        if giver_points >= points_to_gift:
            # 2. Deduct from Giver, Add to Receiver
            cur.execute("UPDATE portal_citizens SET engagement_points = engagement_points - %s WHERE binary_id = %s", (points_to_gift, from_binary_id))
            cur.execute("UPDATE portal_citizens SET engagement_points = engagement_points + %s WHERE binary_id = %s", (points_to_gift, to_binary_id))
            
            conn.commit()
            print(f"🎁 SUCCESS: {points_to_gift} points gifted from ID {from_binary_id} to ID {to_binary_id}.")
            print("🛡️ Sovereign Rule: Pure Help, No Recruitment Commission.")
        else:
            print("❌ Error: Not enough points to gift.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Gifting Error: {e}")

if __name__ == "__main__":
    print("CDC Point Gifting System: Active and Secured.")
