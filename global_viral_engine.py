import sqlite3
import os
import time

# =========================================================
# CODAC SYSTEM: GLOBAL VIRAL ENGINE (FINAL INTEGRATED)
# PLATFORM: SQLite (Termux Compatible)
# =========================================================

class GlobalViralEngine:
    def __init__(self):
        # Pointing to the SAME database as the other engines
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
        """
        Deploys the 'Hayahay' Brand Message into the System Configuration.
        """
        master_message = f"""
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

        📺 WATCH AND SHARE HERE: {self.youtube_channel}

        While you watch, you strengthen our network.
        The old "luxury" is now "help" for the transformation of your life and the world.
        """

        conn = self._connect_db()
        cursor = conn.cursor()

        try:
            # 1. Ensure Config Table Exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_config (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)

            # 2. Deploy Message and Link
            cursor.execute("INSERT OR REPLACE INTO system_config (key, value) VALUES (?, ?)",
                           ('master_viral_msg', master_message))

            cursor.execute("INSERT OR REPLACE INTO system_config (key, value) VALUES (?, ?)",
                           ('official_youtube_link', self.youtube_channel))

            conn.commit()
            print(" [✅] VIRAL ENGINE: 'Hayahay' Message & YouTube Link Successfully Deployed.")

        except Exception as e:
            print(f" [❌] DEPLOYMENT ERROR: {e}")

        finally:
            conn.close()

    def get_global_depth(self):
        conn = self._connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT MAX(current_level) FROM active_members")
            result = cursor.fetchone()
            return result[0] if result and result[0] else 0
        except:
            return 0
        finally:
            conn.close()

# =========================================================
# EXECUTE DEPLOYMENT
# =========================================================
if __name__ == "__main__":
    engine = GlobalViralEngine()
    print(" [🚀] CODAC GLOBAL ENGINE STARTING...")
    
    # Deploy logic
    engine.deploy_viral_message()

    print(f" [📺] OFFICIAL LINK: {engine.youtube_channel}")
    print(" [ℹ️] SYSTEM READY FOR GLOBAL TRAFFIC")
