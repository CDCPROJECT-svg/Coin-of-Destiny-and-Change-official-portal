import sqlite3
import os

class CollectorRoleFixer:
    def __init__(self):
        self.db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def correct_roles(self):
        conn = self._connect()
        cursor = conn.cursor()
        
        print("\033[H\033[J", end="")
        print("=========================================================")
        print("      🛠️ CODAC ROLE CORRECTION PROTOCOL")
        print("=========================================================")

        # 1. REMOVE COLLECTOR FROM 'THE RACE' (User Tasks)
        # Ito ang nagpapalabas sa kanya sa Top Ranking. Tatanggalin natin.
        target = "COLLECTOR-001"
        cursor.execute("DELETE FROM user_tasks WHERE user_id=?", (target,))
        
        if cursor.rowcount > 0:
            print(f" [✅] REMOVED '{target}' from Ranking/Tasks.")
            print(f"      Status: No longer a 'Player'. No Portal Access.")
        else:
            print(f" [ℹ️] '{target}' was not in the ranking (Clean).")

        # 2. ENSURE COLLECTOR EXISTS AS A 'WALLET' ONLY
        # Dapat nasa active_members pa rin siya para matanggap ang locked coins
        # Pero ang status niya ay SYSTEM_VAULT
        cursor.execute("""
            INSERT INTO active_members (user_id, status, trading_points, locked_balance)
            VALUES (?, 'SYSTEM_VAULT', 0.0, 0.0)
            ON CONFLICT(user_id) DO UPDATE SET status='SYSTEM_VAULT';
        """, (target,))
        
        print(f" [💰] CONFIRMED '{target}' as System Vault.")
        print(f"      Function: Catchment for Locked CODAC Coins.")

        # 3. VERIFY THE NEW RANKING (Founder should be alone at Top)
        print("\n [⚔️] VERIFYING LEADERBOARD (Who is Rank 1?)...")
        cursor.execute("""
            SELECT user_id, tasks_completed_at 
            FROM user_tasks 
            WHERE tasks_completed_at IS NOT NULL 
            ORDER BY tasks_completed_at ASC 
            LIMIT 3
        """)
        rankings = cursor.fetchall()
        
        print(f" {'RANK':<5} | {'USER ID':<20} | {'STATUS'}")
        print("-" * 50)
        for rank, (uid, time_score) in enumerate(rankings, 1):
            status = "👑 FOUNDER (GOD MODE)" if uid == "FOUNDER-001" else "MEMBER"
            print(f" {rank:<5} | {uid:<20} | {status}")

        conn.commit()
        conn.close()

if __name__ == "__main__":
    fixer = CollectorRoleFixer()
    fixer.correct_roles()
