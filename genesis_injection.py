import psycopg2

def inject_elites():
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres.xzbozofttuvyijeimxkj',
        password='dnHmzMkSQhvMmCj8',
        host='aws-1-ap-south-1.pooler.supabase.com',
        port='6543',
        sslmode='require'
    )
    cur = conn.cursor()

    print("🚀 Injecting Elite Core...")
    
    for b_id in range(1, 386):
        # Determine Level (simplified mapping based on our audit)
        if b_id == 1: level = 1
        elif b_id <= 3: level = 2
        elif b_id <= 7: level = 3
        elif b_id <= 15: level = 4
        elif b_id <= 31: level = 5
        elif b_id <= 63: level = 6
        elif b_id <= 127: level = 7
        elif b_id <= 181: level = 8
        else: level = 9 # The 204 Countries

        # Apply your Specific Design: CDC-A00009L-000-000-182
        entry_str = str(b_id).zfill(9)
        formatted_id = f"CDC-A0{level}L-{entry_str[-9:-6]}-{entry_str[-6:-3]}-{entry_str[-3:]}"
        
        cur.execute("""
            INSERT INTO portal_citizens (binary_id, designed_id, entry_level, full_name, is_elite)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (binary_id) DO UPDATE SET designed_id = EXCLUDED.designed_id;
        """, (b_id, formatted_id, level, f"ELITE_ACCOUNT_{b_id}", True))

    conn.commit()
    print("✅ PHASE 2 COMPLETE: 385 Elites are Locked and Loaded.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    inject_elites()
