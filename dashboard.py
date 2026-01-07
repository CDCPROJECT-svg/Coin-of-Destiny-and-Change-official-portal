import os

def show_dashboard(level, project, status, wallet_usdt, wallet_cdc):
    os.system('clear')
    print("=====================================================")
    print("          CDC COIN OF DESTINY & CHANGE")
    print("  'Empowering Communities, Creating Wealth...' ")
    print("=====================================================")
    print(f" PROJECT {project}: LEVEL {level} / {28 if project == 1 else 25}")
    print(f" REWARD WALLET: {wallet_usdt} USDT")
    print(f" CDC COIN WALLET: {wallet_cdc} CDC")
    print(f" STATUS: {status}")
    print("-----------------------------------------------------")
    print(" [WATCH YT] [LIKE] [SHARE] -> [CLAIM 8%]")
    print("=====================================================")

# Example Call
show_dashboard(7, 1, "⚠️ VERIFICATION REQUIRED", "18,888", "0.00")
