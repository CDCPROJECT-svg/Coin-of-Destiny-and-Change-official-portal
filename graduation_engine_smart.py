import sqlite3
import os

class SmartGraduationEngine:
    def __init__(self):
        self.db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def calculate_required_usdt(self, current_level):
        base = 18888.0
        if current_level == 1: return base
        elif 2 <= current_level <= 17: return base + ((current_level - 1) * 10000.0)
        elif current_level == 18: return 0.0 # Hayahay
        return 999999.0

    def process_graduation(self, user_id):
        conn = self._connect()
        c = conn.cursor()
        try:
            c.execute("SELECT grand_reward_total, current_level FROM active_members WHERE user_id=?", (user_id,))
            row = c.fetchone()
            if not row: return "USER_NOT_FOUND"
            
            points, level = row
            target = self.calculate_required_usdt(level)

            if level == 18:
                return "GRADUATED_HAYAHAY_MODE"
            elif points >= target:
                new_lvl = level + 1
                c.execute("UPDATE active_members SET current_level=? WHERE user_id=?", (new_lvl, user_id))
                conn.commit()
                return f"PROMOTED_TO_LEVEL_{new_lvl}"
            else:
                return "IN_PROGRESS"
        finally:
            conn.close()
