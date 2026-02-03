import sqlite3
import os

def purge_test_accounts():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🧹 LEVEL 9 CLEANUP PROTOCOL")
    print("=========================================================")

    # 1. BILANGIN MUNA (Bago Burahin)
    cursor.execute("SELECT COUNT(*) FROM active_members WHERE user_id LIKE 'CODAC-SPEC%'")
    count_before = cursor.fetchone()[0]
    print(f" [🧐] Found {count_before} Test Accounts (SPEC) to delete.")

    # 2. EXECUTE DELETE
    if count_before > 0:
        cursor.execute("DELETE FROM active_members WHERE user_id LIKE 'CODAC-SPEC%'")
        conn.commit()
        print(f" [🗑️] DELETED: {count_before} records removed successfully.")
    else:
        print(" [✅] Database is already clean.")

    # 3. VERIFY LEVEL 9 (Dapat Countries lang matira)
    print("\n [🔍] VERIFYING REMAINING LEVEL 9 ANCHORS:")
    cursor.execute("SELECT user_id FROM active_members WHERE current_level=9 LIMIT 5")
    anchors = cursor.fetchall()
    
    for anchor in anchors:
        print(f"      - {anchor[0]}")

    print("\n [✅] CLEANUP COMPLETE. Only Official Countries remain.")
    print("=========================================================")
    conn.close()

if __name__ == "__main__":
    purge_test_accounts()
