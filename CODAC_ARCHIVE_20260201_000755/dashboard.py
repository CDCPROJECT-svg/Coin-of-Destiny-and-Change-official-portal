import os

def show_dashboard(level, project, status, wallet_usdt, wallet_codac):
    os.system('clear')
    print("=====================================================")
    print("          CODAC COIN OF DESTINY & CHANGE")
    print("  'Empowering Communities, Creating Wealth...' ")
    print("=====================================================")
    print(f" PROJECT {project}: LEVEL {level} / {28 if project == 1 else 25}")
    print(f" REWARD WALLET: {wallet_usdt} USDT")
    print(f" CODAC COIN WALLET: {wallet_codac} CODAC")
    print(f" STATUS: {status}")
    print("-----------------------------------------------------")
    print(" [WATCH YT] [LIKE] [SHARE] -> [CLAIM 8%]")
    print("=====================================================")

# Example Call
show_dashboard(7, 1, "⚠️ VERIFICATION REQUIRED", "18,888", "0.00")
