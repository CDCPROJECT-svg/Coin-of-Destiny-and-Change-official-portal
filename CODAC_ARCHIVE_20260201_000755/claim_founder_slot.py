import psycopg2

def claim_slot():
    print("🛡️ Securing Slot 386 for Master Founder...")
    try:
        conn = psycopg2.connect(
            dbname='postgres', user='postgres.xzbozofttuvyijeimxkj',
            password='dnHmzMkSQhvMmCj8', host='aws-1-ap-south-1.pooler.supabase.com',
            port='6543', sslmode='require'
        )
        cur = conn.cursor()

        # I-check muli kung may 386 na (Safety First)
        cur.execute("SELECT binary_id FROM portal_citizens WHERE binary_id = 386;")
        if not cur.fetchone():
            # I-insert ang ID 386
            cur.execute("""
                INSERT INTO portal_citizens 
                (binary_id, username, role, project_id, level_depth, reward_wallet, codac_coin_wallet) 
                VALUES (386, 'MASTER FOUNDER', 'ADMIN', 1, 0, 18888, 0);
            """)
            conn.commit()
            print("✅ SUCCESS: ID 386 is now ACTIVE. You are now the Root of the Tree.")
        else:
            print("ℹ️ ID 386 is already occupied.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    claim_slot()
