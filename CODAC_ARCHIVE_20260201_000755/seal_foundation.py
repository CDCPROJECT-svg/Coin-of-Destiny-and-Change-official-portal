import psycopg2                                    

def seal_all():
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

        print("🛡️ Sealing L1-L8 Foundation...")

        for b_id in range(1, 182):
            # Determine Level and Tag based on your blueprint
            if b_id <= 127: 
                lv, tag, name = "07", "GLB", f"MGMT_{b_id}"
            else: 
                # Level 8 Infrastructure
                lv = "08"
                if 152 <= b_id <= 159: tag = "BUYBK"
                elif 160 <= b_id <= 167: tag = "BCKUP"
                else: tag = "SYS"
                name = f"INFRA_{b_id}"

            entry_str = str(b_id).zfill(9)
            did = f"CODAC-A{lv}L-{tag}-{entry_str[-9:-6]}-{entry_str[-6:-3]}-{entry_str[-3:]}"

            cur.execute("""
                UPDATE portal_citizens
                SET designed_id = %s, full_name = %s, is_elite = TRUE, entry_level = %s
                WHERE binary_id = %s
            """, (did, name, int(lv), b_id))

        conn.commit()
        print("✅ MISSION COMPLETE: IDs 1 to 181 are now Sovereign.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    seal_all()
