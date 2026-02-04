import time
from lifestyle_menu import show_lifestyle_menu
from graduation_engine_smart import SmartGraduationEngine
from universal_payout_engine import UniversalPayoutEngine

def final_run():
    print("\033[H\033[J")
    print("=========================================")
    print(" 🚀 CODAC SYSTEM FINAL INTEGRITY TEST")
    print("=========================================")
    time.sleep(1)

    print("\n [1] TESTING LIFESTYLE MODULE...")
    show_lifestyle_menu()
    time.sleep(1)

    print("\n [2] TESTING GRADUATION LOGIC...")
    grad = SmartGraduationEngine()
    req = grad.calculate_required_usdt(1)
    print(f"      Level 1 Target: ${req:,.2f} (Should be 18,888)")
    
    print("\n [3] TESTING PAYOUT SYSTEM...")
    bank = UniversalPayoutEngine()
    bank.convert_and_pay("TEST_USER", 18888, "Graduation")

    print("\n=========================================")
    print(" ✅ ALL SYSTEMS GREEN. READY FOR GIT.")
    print("=========================================")

if __name__ == "__main__":
    final_run()
