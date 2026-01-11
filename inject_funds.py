import json
import os
import sys

def update_balance(target_id, cdc="0.00", usdt="0.00", fiat="0.00", points="0", currency="USD"):
    folder = 'binary_core'
    file_path = os.path.join(folder, 'live_earnings.json')
    if not os.path.exists(folder): os.makedirs(folder)

    if os.path.exists(file_path):
        with open(file_path, 'r') as f: data = json.load(f)
    else: data = {}

    data[target_id] = {
        "cdc": f"{float(cdc):,.2f}",
        "usdt": f"{float(usdt):,.2f}",
        "fiat": f"{float(fiat):,.2f}",
        "currency": currency,
        "points": f"{int(points):,}"
    }
    
    with open(file_path, 'w') as f: json.dump(data, f, indent=4)
    print(f"✅ UPDATED: {target_id} | CDC: {cdc} | USDT: {usdt} | {currency}: {fiat} | Points: {points}")

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: python3 inject_funds.py [ID] [CDC] [USDT] [FIAT] [POINTS] [CURRENCY]")
        print("Example: python3 inject_funds.py CDC-C1A0001AIOIN 1000000 500000 250000 10000 USD")
    else:
        update_balance(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
