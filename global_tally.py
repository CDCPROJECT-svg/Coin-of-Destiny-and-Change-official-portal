import psycopg2

def get_global_summary():
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

        # Grouping users by Country and Status
        query = """
            SELECT country_name, status, COUNT(*) 
            FROM citizens 
            GROUP BY country_name, status
            ORDER BY COUNT(*) DESC;
        """
        cur.execute(query)
        rows = cur.fetchall()

        print("\n--- 🌍 CDC GLOBAL CITIZEN TALLY (204 COUNTRIES) ---")
        print(f"{'COUNTRY':<20} | {'STATUS':<20} | {'COUNT':<5}")
        print("-" * 50)
        
        for row in rows:
            country = row[0] if row[0] else "Unknown/VPN"
            print(f"{country:<20} | {row[1]:<20} | {row[2]:<5}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Dashboard Error: {e}")

if __name__ == "__main__":
    get_global_summary()
