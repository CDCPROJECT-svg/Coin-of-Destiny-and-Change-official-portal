import sqlite3
import os

# =========================================================
# CODAC MASTER REWARDS ENGINE (CYCLE 2 - UNLI INCENTIVES)
# UPDATE: Every Leadership Level (1-18) gets the 17,777 Bonus
# =========================================================

class MasterRewardsEngine:
    def __init__(self):
        self.db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
        
        # INCENTIVE CONFIGURATION
        # FIXED BUDGET per Level: 17,777 USDT worth of CODAC Coin
        self.incentive_budget = 17777.0 
        self.incentive_currency = "USDT worth of CODAC COIN"
        self.choices = ["🚗 CAR", "✈️ TRAVEL", "🏥 HEALTHCARE"]

    def get_reward_specs(self, level):
        base_usdt = 18888.0
        step_up = 10000.0
        
        # LOGIC: ALL LEVELS (1 to 18) now have "has_incentive: True"
        
        # LEVEL 1: Base Reward + Incentive
        if level == 1:
            return {
                "cash_target": base_usdt,
                "incentive_val": self.incentive_budget,
                "has_incentive": True,
                "note": "Leadership Level 1 (Start of Abundance)"
            }
            
        # LEVEL 2 - 17: Progressive Cash + CONTINUOUS INCENTIVE
        elif 2 <= level <= 17:
            target = base_usdt + ((level - 1) * step_up)
            return {
                "cash_target": target,
                "incentive_val": self.incentive_budget, # ENABLED
                "has_incentive": True,                  # ENABLED
                "note": f"Leadership Level {level} (Continuous Rewards)"
            }
            
        # LEVEL 18: GRADUATION (Exit Bonus)
        elif level == 18:
            return {
                "cash_target": 0.0,  # No Task (Hayahay)
                "incentive_val": self.incentive_budget, 
                "has_incentive": True, 
                "note": "GRADUATION: Final Victory Incentive"
            }
            
        return None

    def check_reward_eligibility(self, level):
        specs = self.get_reward_specs(level)
        
        if not specs:
            print(" [⚠️] Invalid Level")
            return

        print("\n=========================================================")
        print(f" 📊 REWARD BREAKDOWN FOR LEVEL {level}")
        print(f"    Mode: {specs['note']}")
        print("=========================================================")
        
        # 1. CASH COMPONENT
        if specs['cash_target'] > 0:
            print(f" 💰 CASH REWARD: {specs['cash_target']:,.2f} USDT")
        else:
            print(f" 💰 CASH REWARD: NONE (Relax Mode / Auto-Carry)")
            
        # 2. INCENTIVE COMPONENT (UNLOCKED FOR ALL)
        if specs['has_incentive']:
            print(f" 🎁 ADDITIONAL INCENTIVE: {specs['incentive_val']:,.2f} {self.incentive_currency}")
            print(f"    👉 Select One: {', '.join(self.choices)}")
            print(f"    (System will convert 17,777 USDT to CODAC Coins)")
            print(f"    STATUS: AVAILABLE 🟢")
        else:
            print(f" 🎁 INCENTIVE: None")
            
        print("=========================================================")

# =========================================================
# SYSTEM VERIFICATION
# =========================================================
if __name__ == "__main__":
    engine = MasterRewardsEngine()
    
    # Verify Level 1
    engine.check_reward_eligibility(1)
    
    # Verify Level 5 (Dati wala ito, ngayon MERON NA!)
    print("\n [🔍] CHECKING MID-LEVEL UPDATE...")
    engine.check_reward_eligibility(5)
    
    # Verify Level 18
    engine.check_reward_eligibility(18)
