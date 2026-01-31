import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def adjust_tally():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Inililipat ang 3 bansa para mabuo ang target mong 86 sa Group B
    to_upgrade = ["Lebanon", "Paraguay", "Bolivia"]
    
    for country in to_upgrade:
        cursor.execute("UPDATE active_members SET gdp_tier = 2 WHERE name LIKE ?", (f"%{country}%",))

    conn.commit()

    cursor.execute("SELECT count(*) FROM active_members WHERE user_id LIKE 'CODAC-A09L%' AND gdp_tier = 1")
    count_a = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM active_members WHERE user_id LIKE 'CODAC-A09L%' AND gdp_tier = 2")
    count_b = cursor.fetchone()[0]

    print(f"\n--- FINAL BLUEPRINT TALLY ---")
    print(f"Group A (Poorest): {count_a} / Target: 118")
    print(f"Group B (Rich/Dev): {count_b} / Target: 86")
    
    if count_a == 118 and count_b == 86:
        print("\n✅ SUCCESS: Blueprint is now perfectly aligned (118/86).")
    conn.close()

if __name__ == "__main__":
    adjust_tally()
