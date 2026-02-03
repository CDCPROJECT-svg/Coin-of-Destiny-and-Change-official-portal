import json

def calculate_codac_split(project_id, gross_reward):
    # 1. Progressive Deduction Rate (1%, 2%, 3%)
    if project_id <= 6:
        rate = 0.01   # 1% Less
    elif project_id <= 12:
        rate = 0.02   # 2% Less
    else:
        rate = 0.03   # 3% Less
    
    total_less = gross_reward * rate
    net_reward = gross_reward - total_less
    
    # 2. Finalized Split Logic (The 25/25/12.5 Split)
    splits = {
        "Portal Treasury (25%)": round(total_less * 0.25, 2),
        "Portal Reserve (25%)": round(total_less * 0.25, 2),
        "Founder (12.5%)": round(total_less * 0.125, 2),
        "Co-Founder (12.5%)": round(total_less * 0.125, 2),
        "Management Team (12.5%)": round(total_less * 0.125, 2),
        "System Maintenance (12.5%)": round(total_less * 0.125, 2)
    }
    
    # 3. Daily Withdrawal Cap (8% of Net)
    daily_cap = round(net_reward * 0.08, 2)
    
    return {
        "Project_ID": project_id,
        "Gross_Reward": gross_reward,
        "Total_Deduction": round(total_less, 2),
        "Net_Payout": round(net_reward, 2),
        "Daily_Withdrawal_Limit": daily_cap,
        "Distribution_Splits": splits,
        "Tax_Disclaimer": "Member is solely responsible for local country taxation."
    }

# --- TEST CASE: Feeding Level (L1) ---
result = calculate_codac_split(1, 18888)
print("\n" + "="*50)
print("       CODAC SOVEREIGN SPLIT ENGINE REPORT")
print("="*50)
print(f"PROJECT LEVEL: {result['Project_ID']}")
print(f"GROSS REWARD:  {result['Gross_Reward']} USDT")
print(f"TOTAL LESS:    {result['Total_Deduction']} USDT")
print(f"NET PAYOUT:    {result['Net_Payout']} USDT")
print(f"DAILY LIMIT:   {result['Daily_Withdrawal_Limit']} USDT")
print("-" * 50)
print("DISTRIBUTION BREAKDOWN:")
for key, val in result['Distribution_Splits'].items():
    print(f" - {key}: {val} USDT")
print("-" * 50)
print(f"NOTICE: {result['Tax_Disclaimer']}")
print("="*50 + "\n")
