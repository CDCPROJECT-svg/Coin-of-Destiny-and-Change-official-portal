import sqlite3
import os
import time

class SmartGraduationEngine:
    def __init__(self):
        self.db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
        # Level 18 is now purely for POSTING/WAITING (No fixed target)
        self.level_18_status = "WAITING_FOR_BATCH" 

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def calculate_required_usdt(self, current_level):
        """
        THE PROGRESSIVE FORMULA (CORRECTED):
        Level 1  = 18,888
        Level 2-17 = Previous + 10k
        Level 18 = 0 (No Task Required / Waiting Area)
        """
        base_reward = 18888.0
        increment = 10000.0
        
        if current_level == 1:
            return base_reward
        
        elif 2 <= current_level <= 17:
            additional = (current_level - 1) * increment
            return base_reward + additional
            
        elif current_level == 18:
            return 0.0  # NO TARGET. FREEDOM STAGE.
            
        return 999999999.0

    def process_graduation(self, user_id):
        conn = self._connect()
        cursor = conn.cursor()
        
        try:
            # Get User Details including current accumulated points
            cursor.execute("SELECT grand_reward_total, current_level, status FROM active_members WHERE user_id=?", (user_id,))
            data = cursor.fetchone()
            
            if not data: return "USER_NOT_FOUND"

            current_points, current_level, status = data
            target_usdt = self.calculate_required_usdt(current_level)
            
            # --- LOGIC FOR LEVEL 18 (THE EASY LIFE) ---
            if current_level == 18:
                print(f"\n [🏖️] STATUS: {user_id} is in LEVEL 18 (HAYAHAY STAGE)")
                print(f"      Current Points: {current_points:,.2f} USDT")
                print(f"      Task Requirement: NONE")
                print(f"      Action: Accumulating points for Cycle II...")
                
                # Check if ready to enter Cycle 2 (Based on your 'Perfect 20th' rule or Batch Logic)
                # For now, we simulate the trigger to enter Cycle 2
                # In real operation, this waits for the batch to complete.
                self._process_cycle_ii_reentry(user_id, current_points, cursor)
                conn.commit()
                return "WAITING_OR_TRANSITIONING"

            # --- LOGIC FOR LEVELS 1-17 (GRIND MODE) ---
            elif current_points >= target_usdt:
                print(f"\n [🏆] TARGET HIT: {user_id} (Level {current_level})")
                print(f"      Target: {target_usdt:,.2f} | Actual: {current_points:,.2f}")
                
                next_level = current_level + 1
                self._promote_user(user_id, next_level, cursor)
                conn.commit()
                return "GRADUATED"
            
            else:
                return "IN_PROGRESS"

        except Exception as e:
            print(f" [❌] Error: {e}")
            return "ERROR"
        finally:
            conn.close()

    def _promote_user(self, user_id, next_level, cursor):
        cursor.execute("UPDATE active_members SET current_level=? WHERE user_id=?", (next_level, user_id))
        print(f" [🚀] PROMOTED: {user_id} -> Level {next_level}")

    def _process_cycle_ii_reentry(self, user_id, carried_points, cursor):
        """
        THE AUTO-CARRY FEATURE:
        Ang points na naipon sa Level 18 ay dadalhin sa Cycle 2.
        """
        print(f" [🔄] INITIATING CYCLE II ENTRY FOR {user_id}...")
        
        if carried_points > 0:
            print(f" [🎒] AUTO-CARRY POINTS DETECTED: {carried_points:,.2f} USDT")
            print(f"      This user starts Cycle II with a HEAD START!")
        
        new_id = f"{user_id}_CY2"
        timestamp = time.time()
        
        # Insert into Main Feeding with the CARRIED POINTS
        cursor.execute("""
            INSERT INTO active_members 
            (user_id, name, current_cycle, current_level, grand_reward_total, join_date, status)
            VALUES (?, ?, 2, 1, ?, ?, 'ACTIVE')
        """, (new_id, "CYCLE_2_VETERAN", carried_points, timestamp))
        
        # Remove from Level 18 list (Graduate)
        cursor.execute("UPDATE active_members SET status='ARCHIVED_CYCLE_1' WHERE user_id=?", (user_id,))
        
        print(f" [🌍] WELCOME BACK! {new_id} entered Main Feeding (Cycle II).")
        print(f"      Starting Balance: {carried_points:,.2f} USDT")

# =========================================================
# FINAL MATH CHECK
# =========================================================
if __name__ == "__main__":
    engine = SmartGraduationEngine()
    print(" [⚙️] CORRECTED LOGIC LOADED: Level 18 'Hayahay' Mode")
    print("-" * 60)
    print(f" {'LEVEL':<10} | {'TARGET (USDT)':<15} | {'NOTE'}")
    print("-" * 60)
    
    # Check 1-17 Logic
    for lvl in range(1, 18):
        target = engine.calculate_required_usdt(lvl)
        print(f" {lvl:<10} | {target:,.2f}       | +10k Progressive")
        
    # Check Level 18 Logic
    l18_target = engine.calculate_required_usdt(18)
    print(f" {18:<10} | {l18_target:<15} | NO TASK / WAITING / AUTO-CARRY")
    print("-" * 60)
