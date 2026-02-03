import sqlite3
import os

def check_ledger_counts():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\n========================================")
    print("      📊 MASTER LEDGER AUDIT")
    print("========================================")

    # 1. FOUNDER
    cursor.execute("SELECT COUNT(*) FROM active_members WHERE current_level=1")
    founder = cursor.fetchone()[0]

    # 2. PIONEERS (VIPs Level 2-8)
    cursor.execute("SELECT COUNT(*) FROM active_members WHERE current_level BETWEEN 2 AND 8")
    pioneers = cursor.fetchone()[0]

    # 3. COUNTRIES (Level 9)
    cursor.execute("SELECT COUNT(*) FROM active_members WHERE current_level=9")
    countries = cursor.fetchone()[0]

    total = founder + pioneers + countries

    print(f" 👑 FOUNDER (L1):       {founder}")
    print(f" 📜 PIONEERS (L2-L8):   {pioneers}")
    print(f" 🌍 COUNTRIES (L9):     {countries}")
    print("----------------------------------------")
    print(f" 📈 TOTAL ACCOUNTS:     {total}")
    print("========================================\n")

    # SHOW SAMPLE DATA (Para makita mo kung tama ang format)
    if pioneers > 0:
        print(" [🔍] SAMPLE PIONEER: ")
        cursor.execute("SELECT user_id FROM active_members WHERE current_level BETWEEN 2 AND 8 LIMIT 1")
        print(f"      - {cursor.fetchone()[0]}")
    
    if countries > 0:
        print(" [🔍] SAMPLE COUNTRY: ")
        cursor.execute("SELECT user_id FROM active_members WHERE current_level=9 LIMIT 1")
        print(f"      - {cursor.fetchone()[0]}")

    conn.close()

if __name__ == "__main__":
    check_ledger_counts()
