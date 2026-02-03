import os

def check_engine():
    # Hanapin ang script
    engine_path = os.path.expanduser("~/codac-coin_portal/global_viral_engine.py")
    
    if not os.path.exists(engine_path):
        print("❌ Hindi mahanap ang 'global_viral_engine.py'")
        return

    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🌍 GLOBAL VIRAL ENGINE: LOGIC INSPECTION")
    print("=========================================================")
    
    with open(engine_path, 'r') as f:
        content = f.read()
        
    # Check key components
    keywords = {
        "MAX_LEVEL": "Level Cap Checker",
        "RE_ENTRY": "Graduation Re-entry Logic",
        "COUNTRY_LIST": "204 Countries Support",
        "AUTO_FILL": "Auto-Placement Logic"
    }
    
    for key, desc in keywords.items():
        if key in content or key.lower() in content:
            print(f" [✅] DETECTED: {desc}")
        else:
            print(f" [⚠️] MISSING:  {desc}")

    print("-" * 57)
    print(" [!] NOTE: This engine must support 'High Velocity' inserts")
    print("     to handle 500 Million records efficiently.")
    print("=========================================================")

if __name__ == "__main__":
    check_engine()
