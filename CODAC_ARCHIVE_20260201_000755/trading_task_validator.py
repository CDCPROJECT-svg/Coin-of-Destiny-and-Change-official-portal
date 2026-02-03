import sys

def check_trading_status(current_level, current_cycle, total_volume_usdt):
    # 1. Determine Trading Percentage based on Cycle
    # Logic: Cycle N = N%. Max is 8% (Cycle 8 onwards).
    if current_cycle >= 8:
        trade_percent = 0.08  # Fixed Max at 8%
        percent_label = "8%"
    else:
        trade_percent = current_cycle / 100.0
        percent_label = f"{current_cycle}%"

    # 2. Calculate the Grand Reward for the specific Level
    # Formula: 18,888 + (Level - 1) * 10,000
    base_reward = 18888 + (current_level - 1) * 10000

    # 3. Calculate Required Trading Volume
    required_volume = base_reward * trade_percent

    # 4. Determine Status
    remaining_volume = required_volume - total_volume_usdt
    is_complete = total_volume_usdt >= required_volume

    # 5. Output for System / Dashboard
    print(f"\n--- 📉 TRADING TASK AUDIT (Level {current_level} | Cycle {current_cycle}) ---")
    print(f"💰 Target Grand Reward:   {base_reward:,.2f} USDT")
    print(f"📊 Rule:                  {percent_label} of Reward")
    print(f"📉 Required Volume:       {required_volume:,.2f} USDT (Buy & Sell)")
    print(f"📈 Actual Volume Traded:  {total_volume_usdt:,.2f} USDT")

    if is_complete:
        print("✅ STATUS: TASK COMPLETE! (Liquidity Requirement Met)")
        return True
    else:
        print(f"❌ STATUS: INCOMPLETE. (Trade {remaining_volume:,.2f} USDT more)")
        return False

# Test Scenarios (Simulation)
if __name__ == "__main__":
    # Scenario A: Cycle 1 Member (1% Rule)
    # Reward 18,888 -> Needs 188.88
    # User traded 200.00 (PASADO)
    check_trading_status(current_level=1, current_cycle=1, total_volume_usdt=200.00)

    # Scenario B: Cycle 2 Member (2% Rule)
    # Reward 18,888 -> Needs 377.76
    # User traded 200.00 (BAGSAK - Kulang pa)
    check_trading_status(current_level=1, current_cycle=2, total_volume_usdt=200.00)

    # Scenario C: Cycle 9 Member (Max 8% Rule)
    # Reward 18,888 -> Needs 1,511.04
    # User traded 1,600.00 (PASADO)
    check_trading_status(current_level=1, current_cycle=9, total_volume_usdt=1600.00)
