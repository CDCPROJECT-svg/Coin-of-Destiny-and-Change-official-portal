import os

def show_table():
    print("\033[H\033[J", end="")
    print("=========================================================================")
    print("   🏆 CODAC MILESTONE REWARDS SCHEDULE (1K to 1B)")
    print("=========================================================================")
    print(f" {'LVL':<5} | {'SUBSCRIBERS':<18} | {'REWARD':<8} | {'CUMULATIVE':<15}")
    print("-------------------------------------------------------------------------")

    milestones = [
        (1000, 8), (10000, 8), (50000, 8), (100000, 8),
        (500000, 4), (1000000, 4), (5000000, 4), (10000000, 4), (50000000, 4),
        (100000, 2), (500000, 2), (1000000, 1) # Simplified for display
    ]
    
    # Redefining specifically for the display based on your 1K-1B table
    full_milestones = [
        (1000, 8), (10000, 8), (50000, 8), (100000, 8),
        (500000, 4), (1000000, 4), (5000000, 4), (10000000, 4), (50000000, 4),
        (100000000, 2), (500000000, 2), (1000000000, 1)
    ]

    total = 0
    for i, (subs, reward) in enumerate(full_milestones, 1):
        total += reward
        sub_str = "{:,}".format(subs)
        print(f" {i:<5} | {sub_str:<18} | {reward:<8} | {total:<10} CODAC")

    print("=========================================================================")
    print(f" ✨ GRAND TOTAL POTENTIAL: {total} CODAC / MEMBER")
    print("=========================================================================")
    print(" 🔒 MANDATORY RULE: 1.00 CODAC Mandatory 8-Year Lock for ALL NEW members")
    print("    upon their first milestone claim (Pioneer Activation).")
    print("=========================================================================")
    print("\n   📢  M I S S I O N   R E Q U I R E D :")
    print("   ----------------------------------------------------------------------")
    print("   👉 Share @CODACCoinPortalOfficialchannel to unlock next milestone")
    print("   ----------------------------------------------------------------------")

if __name__ == "__main__":
    show_table()
