import sqlite3
import os

def surgical_trim():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=========================================================")
    print("      ✂️  DATABASE SURGERY: REMOVING DUPLICATES")
    print("=========================================================")

    # 1. FIX FOUNDERS (Retain only 'FOUNDER-001', delete others)
    print(" [👑] Fixing Founder Overflow (Target: 1)...")
    cursor.execute("DELETE FROM active_members WHERE current_level=1 AND user_id != 'FOUNDER-001'")
    deleted_founders = cursor.rowcount
    print(f"      - Removed {deleted_founders} fake/duplicate founders.")

    # 2. REMOVE GHOSTS (Accounts with invalid levels or weird IDs)
    # Tatanggalin natin ang anumang hindi Level 1-9
    print(" [👻] Hunting Ghost Accounts...")
    cursor.execute("DELETE FROM active_members WHERE current_level NOT BETWEEN 1 AND 9")
    deleted_ghosts = cursor.rowcount
    print(f"      - Removed {deleted_ghosts} glitched accounts.")

    conn.commit()

    # 3. FINAL AUDIT
    cursor.execute("SELECT COUNT(*) FROM active_members")
    final_total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM active_members WHERE current_level=1")
    cnt_founder = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM active_members WHERE current_level BETWEEN 2 AND 8")
    cnt_pioneers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM active_members WHERE current_level=9")
    cnt_countries = cursor.fetchone()[0]

    print("---------------------------------------------------------")
    print(f" 📊 FINAL RESULT (DAPAT 712):")
    print(f"    👑 Founder:   {cnt_founder}   (Target: 1)")
    print(f"    📜 Pioneers:  {cnt_pioneers} (Target: 507)")
    print(f"    🌍 Countries: {cnt_countries} (Target: 204)")
    print(f"    -------------------------")
    print(f"    ✅ TOTAL NODES: {final_total}")
    print("=========================================================")
    conn.close()

if __name__ == "__main__":
    surgical_trim()
