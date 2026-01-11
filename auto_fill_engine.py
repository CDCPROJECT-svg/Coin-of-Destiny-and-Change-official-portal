import psycopg2

def register_and_update_counts(new_member_id, sponsor_id):
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

        # 1. Hanapin ang path pataas (Ancestry) hanggang 20 levels
        # Ginagamit natin ang Recursive Common Table Expression (CTE)
        cur.execute("""
            WITH RECURSIVE uplines AS (
                SELECT parent_id, 1 as level
                FROM binary_tree
                WHERE member_id = %s
                UNION ALL
                SELECT bt.parent_id, u.level + 1
                FROM binary_tree bt
                JOIN uplines u ON bt.member_id = u.parent_id
                WHERE u.level < 20 AND bt.parent_id IS NOT NULL
            )
            UPDATE portal_citizens
            SET downline_count = downline_count + 1
            WHERE binary_id IN (SELECT parent_id FROM uplines);
        """, (new_member_id,))

        conn.commit()
        print(f"✅ Success: Member {new_member_id} registered. Ancestry counts updated.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Counter Error: {e}")

if __name__ == "__main__":
    # Sample logic trigger
    print("CDC Auto-Fill Engine: Monitoring 20-Level Binary Integrity...")
