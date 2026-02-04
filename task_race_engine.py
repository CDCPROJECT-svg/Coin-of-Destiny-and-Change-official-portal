import sqlite3
import os
import time

class TaskRaceEngine:
    def __init__(self):
        self.db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

    def mark_complete(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS race_results (user_id TEXT PRIMARY KEY, finish_time REAL)")
        try:
            c.execute("INSERT INTO race_results VALUES (?, ?)", (user_id, time.time()))
            conn.commit()
            print(f" [🏁] {user_id} FINISHED THE RACE!")
        except:
            print(f" [ℹ️] {user_id} already finished.")
        conn.close()
