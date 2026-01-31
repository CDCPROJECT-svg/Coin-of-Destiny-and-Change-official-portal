import sys

def check_merchant_status(current_level, total_usdt_spent):
    # 1. Calculate the Grand Reward for the specific Level
    # Formula: 18,888 + (Level - 1) * 10,000
    base_reward = 18888 + (current_level - 1) * 10000
    
    # 2. Calculate the 2% Required Spend
    required_spend = base_reward * 0.02
    
    # 3. Calculate Points Earned (Every 1 USDT spend = 50 Points)
    points_earned = total_usdt_spent * 50
    target_points = required_spend * 50  # This will always match base_reward
    
    # 4. Determine Status
    remaining_spend = required_spend - total_usdt_spent
    is_complete = total_usdt_spent >= required_spend

    # 5. Output for System / Dashboard
    print(f"\n--- 🛍️ MERCHANT SPENDING AUDIT (Level {current_level}) ---")
    print(f"💰 Target Grand Reward:  {base_reward:,.2f} USDT")
    print(f"💳 Required Spend (2%):  {required_spend:,.2f} USDT")
    print(f"🛒 Actual Spend:         {total_usdt_spent:,.2f} USDT")
    print(f"💎 Points Accumulated:   {points_earned:,.0f} / {target_points:,.0f}")
    
    if is_complete:
        print("✅ STATUS: TASK COMPLETE! (Ready for Reward)")
        return True
    else:
        print(f"❌ STATUS: INCOMPLETE. (Spend {remaining_spend:,.2f} USDT more)")
        return False

# Test Scenarios (Simulation)
if __name__ == "__main__":
    # Test Level 1 Member who spent exact 377.76 USDT
    print("Testing Level 1 Member (Exact Spend):")
    check_merchant_status(1, 377.76)

    # Test Level 2 Member (Reward is 28,888) who only spent 100 USDT
    print("\nTesting Level 2 Member (Partial Spend):")
    check_merchant_status(2, 100.00)
