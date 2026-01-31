import time

class AdvocateValidator:
    def __init__(self):
        # STANDARDS
        self.MIN_DAILY_HOURS = 1.0  # Minimum requirement
    
    def analyze_member_growth(self, user_id, c1_avg_hours, c2_avg_hours, join_date_str):
        print("\033[H\033[J", end="")
        print("=========================================================")
        print(f"      💎 CODAC ELITE MEMBER ANALYZER")
        print("=========================================================")
        print(f" 👤 CANDIDATE: {user_id}")
        print(f" 📅 JOIN DATE: {join_date_str} (Simula't Sapol)")
        
        print("-" * 57)
        print(f" 📊 HISTORICAL DATA:")
        print(f"    Cycle 1 Avg Engagement: {c1_avg_hours} Hours/Day")
        print(f"    Cycle 2 Avg Engagement: {c2_avg_hours} Hours/Day")
        
        # LOGIC 1: CONSISTENCY CHECK
        if c2_avg_hours >= self.MIN_DAILY_HOURS:
            status = "ACTIVE ✅"
        else:
            status = "LAZY ❌"
            
        print(f"    Current Status: {status}")
        
        print("-" * 57)
        print("      ANALYZING GROWTH PATTERN...")
        time.sleep(1)
        
        # LOGIC 2: THE "SUPER-USER" CHECK
        # Did they beat their own record?
        if c2_avg_hours > c1_avg_hours:
            growth_pct = ((c2_avg_hours - c1_avg_hours) / c1_avg_hours) * 100
            
            print(f"\n [🚀] RESULT: POSITIVE GROWTH DETECTED (+{growth_pct:.1f}%)")
            print(f"      Verdict: SUPER PRIME LEADER")
            print(f"      Action: Priority Seating in Perfect Level 20.")
            print(f"      Reason: User is working harder than before!")
            
        elif c2_avg_hours == c1_avg_hours:
            print(f"\n [=] RESULT: STABLE PERFORMANCE")
            print(f"      Verdict: CONSISTENT LEADER")
            print(f"      Action: Standard Seating.")
            
        else:
            print(f"\n [📉] RESULT: DECLINING INTEREST")
            print(f"      Verdict: AT RISK")
            print(f"      Action: Send Motivation Notification.")

        print("=========================================================")

# =========================================================
# SIMULATION: THE LOYALIST SCENARIO
# =========================================================
if __name__ == "__main__":
    validator = AdvocateValidator()
    
    # SCENARIO: 
    # User was engaging 2 hours/day in Cycle 1.
    # Now in Cycle 2, they engage 3.5 hours/day (Lumampas!)
    # Join Date: 2025 (Old member)
    
    validator.analyze_member_growth(
        user_id="LOYAL_LEADER_001", 
        c1_avg_hours=2.0, 
        c2_avg_hours=3.5, 
        join_date_str="2025-09-01"
    )
