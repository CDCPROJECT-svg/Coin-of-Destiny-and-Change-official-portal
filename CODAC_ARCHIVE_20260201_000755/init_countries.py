import json
import os

def initialize_global_system():
    folder = 'binary_core'
    file_path = os.path.join(folder, 'live_earnings.json')
    
    # Mapping a few examples - the system will default others to USD
    # You can expand this list as you go
    currency_map = {
        "0003": "PHP", # Example: Philippines
        "0004": "INR", # Example: India
        "0005": "AED", # Example: UAE
        "0006": "GBP", # Example: UK
        "0007": "EUR", # Example: Germany
    }

    if os.path.exists(file_path):
        with open(file_path, 'r') as f: data = json.load(f)
    else: data = {}

    # Initialize 204 Countries (IDs 0003 to 0206)
    for i in range(3, 207):
        suffix = str(i).zfill(4)
        aioin_id = f"CODAC-C1A{suffix}AIOIN"
        
        # Only set if not already injected with big funds
        if aioin_id not in data:
            data[aioin_id] = {
                "codac": "0.00",
                "usdt": "0.00",
                "fiat": "0.00",
                "currency": currency_map.get(suffix, "USD"),
                "points": "0"
            }

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print("✅ 204 Countries Initialized with Local Currency Wallets.")

initialize_global_system()
