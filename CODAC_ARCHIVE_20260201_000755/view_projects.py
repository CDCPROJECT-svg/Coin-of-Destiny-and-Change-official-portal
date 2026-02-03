import psycopg2

def display_projects():
    try:
        conn = psycopg2.connect(
            dbname='postgres', user='postgres.xzbozofttuvyijeimxkj',
            password='dnHmzMkSQhvMmCj8', host='aws-1-ap-south-1.pooler.supabase.com',
            port='6543', sslmode='require'
        )
        cur = conn.cursor()

        print("\n" + "="*45)
        print("👑 CODAC MASTER PROJECT NAVIGATOR (ID 386)")
        print("="*45)

        # Query para sa binary tree depth at totals
        cur.execute("SELECT COUNT(*), MAX(level_depth) FROM portal_citizens;")
        stats = cur.fetchone()

        print(f"📈 Total Network Population : {stats[0]:,}")
        print(f"🌳 Current Tree Depth       : {stats[1]} / 28 Levels")
        
        # Simbolikong representasyon ng 18 Projects
        print("\n📂 PROJECT STATUS (1-18):")
        for i in range(1, 19):
            status = "✅ ACTIVE" if i <= 2 else "⏳ PENDING" # Halimbawa
            print(f"   Project {i:02d}: {status}")

        print("\n" + "="*45)
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    display_projects()
