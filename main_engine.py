# CODAC GLOBAL ENGINE - 2026
# Rules: P1 = 28 Levels | P2-18 = 25 Levels | 8% Daily Withdrawal

class CODACEngine:
    def __init__(self):
        self.feeding_depth = 28
        self.project_depth = 25
        self.withdrawal_limit = 0.08

    def calculate_reward(self, cycle, project_id):
        base_reward = 18888
        if cycle == 1:
            return base_reward
        else:
            # Progressive 10k increase for Cycle 2 & 3
            if 2 <= project_id <= 17:
                return base_reward + ((project_id - 1) * 10000)
            return base_reward

    def get_deduction(self, project_id):
        if project_id <= 6: return 0.01
        if project_id <= 12: return 0.02
        if project_id <= 17: return 0.03
        return 0.01

engine = CODACEngine()
print("CODAC Engine Updated: Depth and Progressive Reward Logic Active.")
