import json
from datetime import datetime

def validate_monthly_engagement(user_id, watch_hours, points):
    # Requirement: 4hrs/week * 4 weeks = 16 hours/month minimum (Feeding)
    # Target Points: 188,888 (Progressive)
    
    MIN_HOURS_MONTHLY = 16 
    current_month = datetime.now().month
    
    print(f"🔍 Auditing Engagement for Member ID: {user_id}")
    
    # Check 1: Monthly Hours (The "Monthly Reset" Logic)
    if watch_hours >= MIN_HOURS_MONTHLY:
        hr_status = "✅ GREEN (Requirement Met)"
        light_on = True
    else:
        hr_status = f"❌ RED ({watch_hours}/{MIN_HOURS_MONTHLY} hrs completed)"
        light_on = False
        
    # Check 2: Total Points (Accumulated)
    print(f" - Watch Hours: {hr_status}")
    print(f" - Total Points: {points:,} / 188,888")
    
    return {
        "user_id": user_id,
        "indicator_light": "GREEN" if light_on else "GREY",
        "can_proceed": light_on and points >= 188888
    }

# Simulation: Testing a member at 15 hours watch time
status = validate_monthly_engagement(386, 15, 120000)
print("\n[DASHBOARD PREVIEW]")
print(f"Indicator Light: {status['indicator_light']}")
if status['indicator_light'] == "GREY":
    print("Action: Keep watching to turn the light GREEN.")
