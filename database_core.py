import psycopg2

def setup_sovereign_db():
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

        # Creating the Master Citizen Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS portal_citizens (
                binary_id SERIAL PRIMARY KEY,
                designed_id VARCHAR(50) UNIQUE,
                cycle_code CHAR(1) DEFAULT 'A',
                batch_number INT DEFAULT 0,
                entry_level INT,
                full_name VARCHAR(100),
                is_elite BOOLEAN DEFAULT FALSE,
                codac_points_balance DECIMAL(20, 8) DEFAULT 0.0,
                points_umbrella_total DECIMAL(20, 8) DEFAULT 0.0,
                status VARCHAR(20) DEFAULT 'active'
            );
        """)

        conn.commit()
        print("✅ PHASE 1 COMPLETE: Database Core is online.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ DB Setup Error: {e}")

if __name__ == "__main__":
    setup_sovereign_db()
