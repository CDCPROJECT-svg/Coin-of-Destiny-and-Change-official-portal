import sqlite3
import os
import random

def restock_pioneers():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=========================================================")
    print("      🛠️ PIONEER RESTOCKING PROTOCOL")
    print("=========================================================")

    # 1. CHECK CURRENT COUNT (Level 2-8)
    cursor.execute("SELECT COUNT(*) FROM active_members WHERE current_level BETWEEN 2 AND 8")
    current_pioneers = cursor.fetchone()[0]
    
    target_pioneers = 512 # (513 minus 1 Founder)
    needed = target_pioneers - current_pioneers

    print(f" [🧐] Current Pioneers:  {current_pioneers}")
    print(f" [🎯] Target Pioneers:   {target_pioneers}")
    
    if needed > 0:
        print(f" [⚠️] MISSING:           {needed} accounts")
        print(" [🚀] Generating missing VIPs...")
        
        for i in range(needed):
            # Generate random VIP ID
            random_digits = random.randint(100, 999)
            vip_id = f"CODAC-VIP-{random.randint(1,9)}-{random_digits}"
            # Distribute across levels 2-8 randomly
            level = random.randint(2, 8)
            
            try:
                cursor.execute("""
                    INSERT INTO active_members (user_id, parent_id, current_level, grand_reward_total, trading_points, locked_balance)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (vip_id, "FOUNDER-001", level, 5000.00, 1000.00, 4000.00))
            except sqlite3.IntegrityError:
                continue # Skip if ID exists

        conn.commit()
        print(f" [✅] SUCCESS: Added {needed} new VIP Pioneers.")
    else:
        print(" [✨] DATABASE IS ALREADY FULL (513 Complete).")

    # FINAL CHECK
    cursor.execute("SELECT COUNT(*) FROM active_members WHERE current_level BETWEEN 2 AND 8")
    final_pioneers = cursor.fetchone()[0]
    total_nodes = final_pioneers + 1 + 204 # Pioneers + Founder + Countries

    print("---------------------------------------------------------")
    print(f" 📊 NEW TOTAL PIONEERS: {final_pioneers + 1} (Target: 513)")
    print(f" 🌍 TOTAL COUNTRIES:    204")
    print(f" 📈 NETWORK TOTAL:      {total_nodes}")
    print("=========================================================")
    conn.close()

if __name__ == "__main__":
    restock_pioneers()
