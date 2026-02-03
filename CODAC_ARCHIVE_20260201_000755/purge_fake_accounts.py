import sqlite3
import os

def clean_master_ledger():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=========================================================")
    print("      🧹 MASTER LEDGER CLEANUP (REMOVING FILLERS)")
    print("=========================================================")

    # 1. DELETE ARTIFICIAL ACCOUNTS
    # Binubura natin ang mga ginawa kong 'Filler', 'Recovery', at 'Spec'
    cursor.execute("DELETE FROM active_members WHERE user_id LIKE '%FILLER%'")
    deleted_fillers = cursor.rowcount
    
    cursor.execute("DELETE FROM active_members WHERE user_id LIKE '%RECOVERY%'")
    deleted_recovery = cursor.rowcount
    
    cursor.execute("DELETE FROM active_members WHERE user_id LIKE '%SPEC%'")
    deleted_spec = cursor.rowcount

    total_deleted = deleted_fillers + deleted_recovery + deleted_spec

    print(f" [🗑️] Deleted FILLER accounts:   {deleted_fillers}")
    print(f" [🗑️] Deleted RECOVERY accounts: {deleted_recovery}")
    print(f" [🗑️] Deleted SPEC accounts:     {deleted_spec}")
    print("-" * 40)
    print(f" [✅] TOTAL REMOVED: {total_deleted}")

    conn.commit()
    
    # 2. FINAL COUNT (REAL LEDGER ONLY)
    cursor.execute("SELECT COUNT(*) FROM active_members")
    final_count = cursor.fetchone()[0]

    # Breakdown
    cursor.execute("SELECT COUNT(*) FROM active_members WHERE current_level=1")
    founder = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM active_members WHERE current_level BETWEEN 2 AND 8")
    pioneers = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM active_members WHERE current_level=9")
    countries = cursor.fetchone()[0]

    print("=========================================================")
    print(f" 📊 MASTER LEDGER AUTHENTIC COUNT: {final_count}")
    print(f"    👑 Founder:   {founder}")
    print(f"    📜 Pioneers:  {pioneers}")
    print(f"    🌍 Countries: {countries}")
    print("=========================================================")
    conn.close()

if __name__ == "__main__":
    clean_master_ledger()
