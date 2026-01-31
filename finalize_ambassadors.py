import psycopg2

def finalize_9l():
    # Corrected mapping with commas
    mapping = {
        182: ("SDG", "Sudan"),
        183: ("PHP", "Philippines"),
        184: ("USD", "United States"),
        185: ("AED", "United Arab Emirates"),
        186: ("SAR", "Saudi Arabia"),
        187: ("EUR", "France"),
        188: ("GBP", "United Kingdom"),
        189: ("JPY", "Japan"),
        190: ("CNY", "China"),
        191: ("INR", "India")
    }

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

        print("🌍 Finalizing Ambassador Sovereign IDs...")

        for b_id in range(182, 386):
            tag, name = mapping.get(b_id, ("GLB", f"Country_{b_id}"))
            entry_str = str(b_id).zfill(9)
            # CODAC-A09L-[TAG]-000-000-ENTRY
            did = f"CODAC-A09L-{tag}-{entry_str[-9:-6]}-{entry_str[-6:-3]}-{entry_str[-3:]}"
            
            cur.execute("""
                UPDATE portal_citizens 
                SET designed_id = %s, full_name = %s, is_elite = TRUE, entry_level = 9 
                WHERE binary_id = %s
            """, (did, name, b_id))

        conn.commit()
        print("✅ 9th Level Ambassadors Secured.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    finalize_9l()
