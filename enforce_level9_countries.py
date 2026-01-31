import sqlite3
import os

class Level9Enforcer:
    def __init__(self):
        self.db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def execute_force_move(self):
        conn = self._connect()
        cursor = conn.cursor()

        print("\033[H\033[J", end="")
        print("=========================================================")
        print("      🏗️ ARCHITECTURE CORRECTION: LEVEL 9")
        print("      Objective: Move all Countries to Level 9")
        print("=========================================================")

        # 1. GET ALL COUNTRIES
        print(" [1] Fetching Countries...")
        cursor.execute("SELECT user_id FROM active_members WHERE user_id LIKE 'CODAC-A09L%' ORDER BY user_id ASC")
        countries = [r[0] for r in cursor.fetchall()]
        
        if not countries:
            print(" [❌] No Countries found! Check database.")
            return
        
        print(f"      -> Found {len(countries)} Countries to move.")

        # 2. GET POTENTIAL PARENTS (LEVEL 8 VIPs)
        # We need to find nodes that are strictly at Level 8
        print("\n [2] Finding Parents (Level 8 VIPs)...")
        cursor.execute("""
            SELECT user_id FROM active_members 
            WHERE current_level = 8 
            AND user_id NOT LIKE 'CODAC-A09L%'
            ORDER BY user_id ASC
        """)
        level8_parents = [r[0] for r in cursor.fetchall()]

        # SAFETY NET: If Level 8 is empty, we might need to use Level 7 or create Level 8
        if not level8_parents:
            print(" [⚠️] WARNING: No VIPs found at Level 8!")
            print("      Searching for deepest available level...")
            cursor.execute("SELECT MAX(current_level) FROM active_members WHERE user_id NOT LIKE 'CODAC-A09L%'")
            deepest = cursor.fetchone()[0]
            print(f"      -> Deepest VIP Level found is: {deepest}")
            
            cursor.execute(f"SELECT user_id FROM active_members WHERE current_level = {deepest} AND user_id NOT LIKE 'CODAC-A09L%'")
            level8_parents = [r[0] for r in cursor.fetchall()]

        print(f"      -> Found {len(level8_parents)} Parents to anchor Countries.")

        # 3. RE-WIRE: CONNECT COUNTRIES TO LEVEL 8 PARENTS
        print("\n [3] MOVING COUNTRIES TO LEVEL 9...")
        
        parent_index = 0
        total_parents = len(level8_parents)
        
        # We assign roughly evenly, or filling left-to-right
        for country in countries:
            if parent_index >= total_parents:
                parent_index = 0 # Loop back to first parent if we run out (sharing parents)
            
            parent_id = level8_parents[parent_index]
            
            # FORCE UPDATE
            cursor.execute("""
                UPDATE active_members 
                SET current_level = 9, 
                    parent_id = ?, 
                    position = 'AUTO' 
                WHERE user_id = ?
            """, (parent_id, country))
            
            # Move to next parent only after filling Left/Right? 
            # For simplicity, we distribute 1 country per parent first.
            parent_index += 1

        conn.commit()
        conn.close()

        print("-" * 57)
        print(" [✅] REALIGNMENT COMPLETE.")
        print("      All Countries are now strictly at LEVEL 9.")
        print("=========================================================")

if __name__ == "__main__":
    enforcer = Level9Enforcer()
    enforcer.execute_force_move()
