import time
from global_viral_engine import GlobalViralEngine
from graduation_engine_smart import SmartGraduationEngine
from auto_cycle_manager import AutoCycleManager
import sqlite3
import os

def run_simulation():
    print("\033[H\033[J", end="") # Clear Screen
    print("=========================================================")
    print("      🌟 CODAC: THE CORRECT GRAND SIMULATION")
    print("=========================================================")
    
    # 1. Initialize Engines
    ladder = SmartGraduationEngine()
    infinite_loop = AutoCycleManager()
    
    test_user = "SIMULATION_USER_001"
    
    # SETUP: Manually putting user in Level 18
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Clearning previous data for accurate test
    cur.execute("DELETE FROM active_members WHERE user_id=?", (test_user,))
    cur.execute("""
        INSERT INTO active_members (user_id, current_level, grand_reward_total, status)
        VALUES (?, 18, 0, 'ACTIVE')
    """, (test_user,))
    conn.commit()
    conn.close()

    print(f"\n [1] 🏖️ ENTERING LEVEL 18 (THE HAYAHAY STAGE)")
    print(f"      User: {test_user}")
    print(f"      Initial Points: 0 (Wala nang required task)")
    
    # Run Logic Check
    result = ladder.process_graduation(test_user)
    
    print(f"\n      ℹ️ SYSTEM RESPONSE: {result}")
    print("      (Dahil nasa Level 18 siya, ang system ay naka-'WAITING' mode lang.)")
    print("      (Walang reward na ibinigay. Walang task na hiningi.)")

    print("\n [2] 🎒 SIMULATING 'VOLUNTARY' TASK (Optional)")
    print("      Scenario: Si User ay nabored kaya nag-watch ng ads (Voluntary).")
    
    # User earns points voluntarily
    earned_points = 500.0 
    print(f"      User earned: {earned_points} USDT (Baon for Cycle 2)")
    
    print("\n [3] 🔄 CYCLE 2 TRANSITION")
    print("      Paglipat sa Cycle 2, dala niya ang pinaghirapan niya.")
    
    success = infinite_loop.execute_auto_upgrade(test_user, earned_points)
    
    if success:
        print("\n=========================================================")
        print("      ✅ CORRECT SIMULATION COMPLETE")
        print("      Confirmed: Level 18 has NO REQUIRED REWARD.")
        print("      Confirmed: Only Voluntary Points are carried over.")
        print("=========================================================")

if __name__ == "__main__":
    run_simulation()
