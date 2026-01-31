import datetime

class CodacCycleManager:
    def __init__(self):
        # LEVEL LIMITS
        self.limits = {
            "feeder": 28,       # Level I (28 Levels)
            "leadership": 25,   # Level II-XVII (25 Levels)
            "waiting": 21       # Level XVIII (21 Levels - Fixed)
        }
        
        # TITLES (Cycle I)
        self.titles_c1 = {
            1: "Ambassador", 2: "Senior Ambassador", 3: "Executive Ambassador",
            4: "Lead Ambassador", 5: "Regional Governor", 6: "Provincial Governor",
            7: "State Governor", 8: "National Governor", 9: "Federal Governor",
            10: "Continental Governor", 11: "Global Governor", 12: "High Global Governor",
            13: "Sovereign Governor", 14: "Grand Sovereign Governor", 15: "Supreme Council Governor",
            16: "High Supreme Governor", 17: "Grand Supreme Governor", 18: "Supreme Governor"
        }

        # TITLES (Cycle II)
        self.titles_c2 = {
            1: "Ambassador II", 2: "Senior Ambassador II", 3: "Executive Ambassador II",
            4: "Lead Ambassador II", 5: "Regional Governor II", 6: "Provincial Governor II",
            7: "State Governor", 8: "National Governor", 9: "Federal Governor",
            10: "Continental Governor", 11: "Global Governor", 12: "High Global Governor",
            13: "Sovereign Governor", 14: "Grand Sovereign Governor", 15: "Supreme Council Governor",
            16: "High Supreme Governor", 17: "Grand Supreme Governor", 18: "Supreme Governor"
        }

    def get_title(self, level, cycle):
        if cycle == 1: return self.titles_c1.get(level, "Unknown")
        elif cycle == 2: return self.titles_c2.get(level, "Unknown")
        return "Unknown Rank"

    def graduate_member(self, user_data, current_level, current_cycle):
        """
        Moves member to next level, saves history, and RESETS points to 0.
        """
        print(f"--- GRADUATING MEMBER: {user_data['name']} ---")
        
        # Determine Next Step
        if current_level == 18:
            next_level = 1
            next_cycle = current_cycle + 1
        else:
            next_level = current_level + 1
            next_cycle = current_cycle

        # Create New Entry Data (Points Reset to 0)
        new_entry = {
            "id": user_data['id'],
            "name": user_data['name'],
            "cycle": next_cycle,
            "level": next_level,
            "codac_points": 0, 
            "title": self.get_title(next_level, next_cycle)
        }
        return new_entry
