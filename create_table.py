import psycopg2

def create_structure():
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

        # Create the Master Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS portal_citizens (
                binary_id INTEGER PRIMARY KEY,
                designed_id VARCHAR(50) UNIQUE,
                full_name VARCHAR(100),
                upline_ptr INTEGER,
                entry_level INTEGER,
                is_elite BOOLEAN DEFAULT FALSE,
                local_currency_code VARCHAR(10),
                cdc_points_balance DECIMAL(20, 8) DEFAULT 0,
                status VARCHAR(20) DEFAULT 'active',
                cycle_code VARCHAR(5) DEFAULT 'A'
            );
        """)
        
        # Create an initial empty 385 slots so we can UPDATE them later
        print("🏗️ Creating 385 Elite slots...")
        for i in range(1, 386):
            cur.execute("INSERT INTO portal_citizens (binary_id) VALUES (%s) ON CONFLICT DO NOTHING", (i,))

        conn.commit()
        print("✅ DATABASE READY: Table 'portal_citizens' is now live.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Table Error: {e}")

if __name__ == "__main__":
    create_structure()
