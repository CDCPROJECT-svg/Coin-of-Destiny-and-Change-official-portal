import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
REPORT_FILE = "final_audit_report.txt"

def generate_report():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(REPORT_FILE, "w") as f:
        f.write("============================================================\n")
        f.write("            CODAC COIN PORTAL - MASTER AUDIT REPORT         \n")
        f.write("============================================================\n\n")

        # Summary Section
        cursor.execute("SELECT count(*) FROM active_members WHERE user_id LIKE 'CODAC-A09L%' AND gdp_tier = 1")
        count_a = cursor.fetchone()[0]
        cursor.execute("SELECT count(*) FROM active_members WHERE user_id LIKE 'CODAC-A09L%' AND gdp_tier = 2")
        count_b = cursor.fetchone()[0]

        f.write(f"TOTAL COUNTRIES      : 204\n")
        f.write(f"GROUP A (118 Target) : {count_a}\n")
        f.write(f"GROUP B (86 Target)  : {count_b}\n")
        f.write(f"STATUS               : READY (OFF-CHAIN)\n")
        f.write("------------------------------------------------------------\n\n")

        # List Group A
        f.write("--- GROUP A: POOREST/PRIORITY (REWARD: 1,888,888) ---\n")
        cursor.execute("SELECT name, wallet_address FROM active_members WHERE user_id LIKE 'CODAC-A09L%' AND gdp_tier = 1 ORDER BY name ASC")
        for i, row in enumerate(cursor.fetchall(), 1):
            f.write(f"{i:3}. {row[0]:<30} | {row[1]}\n")

        f.write("\n" + "="*60 + "\n\n")

        # List Group B
        f.write("--- GROUP B: DEVELOPED/RICH (REWARD: 888,888) ---\n")
        cursor.execute("SELECT name, wallet_address FROM active_members WHERE user_id LIKE 'CODAC-A09L%' AND gdp_tier = 2 ORDER BY name ASC")
        for i, row in enumerate(cursor.fetchall(), 1):
            f.write(f"{i:3}. {row[0]:<30} | {row[1]}\n")

    conn.close()
    print(f"\nSUCCESS: Audit report generated: {REPORT_FILE}")

if __name__ == "__main__":
    generate_report()
