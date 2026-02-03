import os

# The content of the Global Viral Engine
engine_code = r"""import sqlite3
import os
import time

# =========================================================
# CODAC SYSTEM: GLOBAL VIRAL ENGINE (FINAL)
# INCLUDES: Level 28 Logic + Viral Message + YouTube Link
# =========================================================

class GlobalViralEngine:
    def __init__(self):
        self.db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
        self.max_depth = 28
        
        # OFFICIAL ASSETS
        self.youtube_channel = "https://youtube.com/@codaccoinportalofficialchannel?si=qnVtzlVMBP88ZtXX"
        self.official_emails = {
            "alerts": "alerts@codac-coin.com",
            "channels": "channels@codac-coin.com",
            "admin": "admin@codac-coin.com",
            "notify": "notify@codac-coin.com"
        }

    def _connect_db(self):
        return sqlite3.connect(self.db_path)

    def deploy_viral_message(self):
        # The viral message content (Brand Identity)
        master_message = '''
        "Akala mo ba, ang paggastos ay sanhi ng pagka-ubos at ang pagiging tambay ay sanhi ng kawalan?
        Sa CODAC, ang bawat gastos at pag tambay mo ay pag-unlad ng lahat."

        To GOD be All the GLORY!.. Welcome to CODAC-Coin, a COIN of DESTINY & CHANGE 
        where life becomes Easy and HAYAHAY.

        This is not just a cryptocurrency; it is a Movement for true freedom.
        Together, let us build a system where watching, spending, and being a consumer
        are no longer causes of poverty—instead, they will bring comfort to all.

        📢 SPREAD THE MESSAGE:
        Please share our YouTube Channel with your family, friends, and colleagues.
        Let us unite to change the world, one viewer at a time.

        📺 WATCH AND SHARE HERE: ''' + self.youtube_channel + '''

        While you watch, you strengthen our network.
        The old "luxury" is now "help" for the transformation of your life and the world.
        '''
        
        conn = self._connect_db()
        cursor = conn.cursor()
        
        try:
            # Using 'key' and 'value' to match your schema
            cursor.execute("INSERT OR REPLACE INTO system_config (key, value) VALUES (?, ?)", 
                           ('master_viral_msg', master_message))
            
            cursor.execute("INSERT OR REPLACE INTO system_config (key, value) VALUES (?, ?)", 
                           ('official_youtube_link', self.youtube_channel))
            
            conn.commit()
            print(" [✅] VIRAL ENGINE: 'Hayahay' Message & YouTube Link Deployed.")
            
        except sqlite3.OperationalError as e:
            # Fallback for safety
            cursor.execute("CREATE TABLE IF NOT EXISTS system_config (key TEXT PRIMARY KEY, value TEXT)")
            cursor.execute("INSERT OR REPLACE INTO system_config (key, value) VALUES (?, ?)", 
                           ('master_viral_msg', master_message))
            conn.commit()
            print(" [✅] RECOVERY: Table created and message deployed.")
            
        finally:
            conn.close()

    def get_global_depth(self):
        conn = self._connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT MAX(current_level) FROM active_members")
            result = cursor.fetchone()
            depth = result[0] if result and result[0] else 0
            return depth
        except:
            return 0
        finally:
            conn.close()
            
    def register_global_member(self, user_id, sponsor_id):
        # Logic to place member
        current_depth = self.get_global_depth()
        if current_depth >= self.max_depth:
            return {"status": "FULL", "msg": "Cycle 1 Full"}
            
        conn = self._connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO active_members (user_id, parent_id, current_level, current_cycle, join_date, status) VALUES (?, ?, ?, ?, ?, ?)", 
            (user_id, sponsor_id, current_depth + 1, 1, time.time(), "ACTIVE"))
            conn.commit()
            return {"status": "SUCCESS", "level": current_depth + 1}
        except Exception as e:
            return {"status": "ERROR", "msg": str(e)}
        finally:
            conn.close()

if __name__ == "__main__":
    engine = GlobalViralEngine()
    print(" [🚀] CODAC GLOBAL ENGINE ONLINE")
    engine.deploy_viral_message()
"""

# Write the file safely
with open("global_viral_engine.py", "w") as f:
    f.write(engine_code)

print("✅ SUCCESS: global_viral_engine.py has been created/repaired.")
