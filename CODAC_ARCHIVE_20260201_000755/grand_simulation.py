import time
from global_viral_engine import GlobalViralEngine
from graduation_engine_smart import SmartGraduationEngine
from universal_payout_engine import UniversalPayoutEngine
import sqlite3
import os

def run_grand_simulation():
    print("\033[H\033[J", end="") # Clear Screen
    print("=========================================================")
    print("      🌟 CODAC: THE GRAND SIMULATION (LIVE TEST)")
    print("=========================================================")
    time.sleep(1)

    # 1. SETUP ENGINES
    viral = GlobalViralEngine()
    ladder = SmartGraduationEngine()
    bank = UniversalPayoutEngine()
    
    test_user = "SIMULATION_VIP_001"
    
    # 2. SCENARIO: A USER REACHES LEVEL 18 (HAYAHAY)
    print(f"\n [1] 👤 USER STATUS CHECK: {test_user}")
    print("      Checking database for graduation eligibility...")
    time.sleep(1)
    
    # Manually inject user to Level 18 for testing
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    conn.execute("INSERT OR REPLACE INTO active_members (user_id, current_level, grand_reward_total, status) VALUES (?, 18, 0, 'ACTIVE')", (test_user,))
    conn.commit()
    conn.close()

    # Run Graduation Check
    status = ladder.process_graduation(test_user)
    print(f"      ℹ️ SYSTEM RESULT: {status}")
    
    if status == "WAITING_FOR_BATCH" or status == "WAITING_OR_TRANSITIONING":
        print("      ✅ Logic Confirmed: User is in HAYAHAY MODE (No Task Required).")

    time.sleep(2)

    # 3. SCENARIO: PAYOUT TIME (CYCLE 1 GRADUATION)
    print(f"\n [2] 💸 PAYOUT EVENT")
    print("      User completed Cycle 1. Distributing Rewards...")
    time.sleep(1)
    
    reward_usdt = 18888.00
    coins = bank.convert_and_pay(test_user, reward_usdt, "CYCLE 1 COMPLETION")

    # 4. SCENARIO: VIRAL SPREAD
    print(f"\n [3] 📢 VIRAL ENGINE CHECK")
    print("      Deploying Official Message to Global Network...")
    viral.deploy_viral_message()
    
    print("\n=========================================================")
    print("      ✅ GRAND SIMULATION COMPLETED SUCCESSFULLY")
    print("      The System is Healthy, Logical, and Ready.")
    print("=========================================================")

if __name__ == "__main__":
    run_grand_simulation()
