import sqlite3
import os
import time
from datetime import datetime

class TaskRaceEngine:
    def __init__(self):
        self.db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
        self.PERFECT_20_LIMIT = 1048576

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def mark_task_complete(self, user_id, task_type):
        """
        Tasks: 'TRADING', 'YOUTUBE', 'MERCHANT'
        """
        conn = self._connect()
        cursor = conn.cursor()
        
        # 1. Ensure User Exists in a 'Task Room' (Virtual Holding Area)
        # Create table if not exists for task tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_tasks (
                user_id TEXT PRIMARY KEY,
                trading_done BOOLEAN DEFAULT 0,
                youtube_done BOOLEAN DEFAULT 0,
                merchant_done BOOLEAN DEFAULT 0,
                tasks_completed_at REAL DEFAULT NULL,
                join_date REAL
            )
        """)
        
        # Insert dummy user if not exists (for simulation)
        cursor.execute("INSERT OR IGNORE INTO user_tasks (user_id, join_date) VALUES (?, ?)", (user_id, time.time()))
        
        # 2. Mark the specific task
        column_map = {
            "TRADING": "trading_done",
            "YOUTUBE": "youtube_done",
            "MERCHANT": "merchant_done"
        }
        
        col = column_map.get(task_type)
        if col:
            cursor.execute(f"UPDATE user_tasks SET {col} = 1 WHERE user_id = ?", (user_id,))
            print(f" [✅] {user_id}: Completed {task_type} Task.")
            
        # 3. CHECK IF ALL TASKS ARE DONE (The Race Logic)
        cursor.execute("SELECT trading_done, youtube_done, merchant_done FROM user_tasks WHERE user_id=?", (user_id,))
        row = cursor.fetchone()
        
        if row and all(row): # If all 3 are True (1)
            # Check if already timestamped
            cursor.execute("SELECT tasks_completed_at FROM user_tasks WHERE user_id=?", (user_id,))
            if cursor.fetchone()[0] is None:
                completion_time = time.time()
                cursor.execute("UPDATE user_tasks SET tasks_completed_at = ? WHERE user_id = ?", (completion_time, user_id))
                print(f" [🏆] RACE FINISHED! {user_id} completed ALL TASKS at {datetime.fromtimestamp(completion_time)}")
        
        conn.commit()
        conn.close()

    def generate_perfect_20_ranking(self):
        """
        This is the JUDGE. It ranks people based on COMPLETION TIME, not Join Date.
        """
        conn = self._connect()
        cursor = conn.cursor()
        
        print("\n=========================================================")
        print("      🏁 CODAC PERFECT 20 LEADERBOARD")
        print("      Criteria: First to Finish Tasks = First in Position")
        print("=========================================================")
        
        # SORT BY completion_time ASCENDING (Oldest time/First to finish is Top 1)
        # We ignore those who haven't finished yet (tasks_completed_at IS NOT NULL)
        cursor.execute("""
            SELECT user_id, tasks_completed_at 
            FROM user_tasks 
            WHERE tasks_completed_at IS NOT NULL 
            ORDER BY tasks_completed_at ASC 
            LIMIT ?
        """, (self.PERFECT_20_LIMIT,))
        
        rankings = cursor.fetchall()
        
        if not rankings:
            print(" [ℹ️] No qualifiers yet. The race is ongoing.")
        else:
            print(f" {'RANK':<5} | {'USER ID':<20} | {'FINISH TIME'}")
            print("-" * 50)
            for rank, (uid, finish_time) in enumerate(rankings, 1):
                ft_str = datetime.fromtimestamp(finish_time).strftime('%H:%M:%S.%f')[:-3]
                print(f" {rank:<5} | {uid:<20} | {ft_str}")
                
        conn.close()

# =========================================================
# SIMULATION: THE RACE (TURTLE VS RABBIT)
# =========================================================
if __name__ == "__main__":
    race = TaskRaceEngine()
    
    # 1. USER A (The Turtle) - Joined FIRST, but works SLOW
    user_a = "USER_NAUNA_PERO_BAGAL"
    print(f"\n--- 🐢 {user_a} joins the system ---")
    race.mark_task_complete(user_a, "TRADING")
    time.sleep(1) # Delay
    
    # 2. USER B (The Rabbit) - Joined LATER, but works FAST
    user_b = "USER_NAHULI_PERO_MABILIS"
    print(f"\n--- 🐇 {user_b} joins the system ---")
    
    # User B finishes everything instantly!
    race.mark_task_complete(user_b, "TRADING")
    race.mark_task_complete(user_b, "YOUTUBE")
    race.mark_task_complete(user_b, "MERCHANT") # FINISH LINE!
    
    time.sleep(1)
    
    # 3. USER A finally finishes later
    print(f"\n--- 🐢 {user_a} continues working... ---")
    race.mark_task_complete(user_a, "YOUTUBE")
    race.mark_task_complete(user_a, "MERCHANT") # FINISH LINE (LATE)
    
    # 4. WHO GETS THE TOP SPOT?
    race.generate_perfect_20_ranking()
