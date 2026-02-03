import time
import random

class UniversalPayoutEngine:
    def __init__(self):
        # SIMULATED MARKET DATA
        # Sa Live System, kukunin ito sa DexScreener o CoinGecko
        self.current_market_price = 2.50  # Example: 1 CODAC = $2.50 USDT

    def convert_and_pay(self, user_id, usdt_amount, reward_type):
        """
        THE GOLDEN RULE:
        Value is pegged in USDT, but Payment is strictly in CODAC COIN.
        """
        print("\033[H\033[J", end="") # Clear Screen
        print("=========================================================")
        print("      💸 CODAC UNIVERSAL PAYOUT SYSTEM")
        print("      Protocol: USDT Value -> CODAC Coin Asset")
        print("=========================================================")

        print(f" 👤 USER: {user_id}")
        print(f" 🏆 REWARD TYPE: {reward_type}")
        print(f" 💲 CLAIM VALUE: {usdt_amount:,.2f} USDT")

        print("-" * 57)
        print(f" [📉] LIVE MARKET PRICE: ${self.current_market_price} per CODAC")
        print("      Converting value...")
        time.sleep(1)

        # CONVERSION FORMULA
        codac_coins_received = usdt_amount / self.current_market_price

        print("-" * 57)
        print(f" [✅] CONVERSION COMPLETE")
        print(f"      You will receive: {codac_coins_received:,.4f} CODAC COINS")
        print("-" * 57)

        print(f" [🚀] SENDING {codac_coins_received:,.4f} CDC TO WALLET...")
        # Simulate Blockchain Transaction
        time.sleep(1.5)

        print("\n=========================================================")
        print("      🎉 PAYOUT SUCCESSFUL!")
        print(f"      The user received CODAC COINS equivalent to")
        print(f"      ${usdt_amount:,.2f} USDT.")
        print("=========================================================")

        return codac_coins_received

# SELF-TEST
if __name__ == "__main__":
    engine = UniversalPayoutEngine()
    engine.convert_and_pay("TEST_USER_001", 18888.00, "LEVEL 1 GRAND REWARD")
