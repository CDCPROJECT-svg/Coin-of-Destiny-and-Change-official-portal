import psycopg2

def show_founder_stats():
    try:
        conn = psycopg2.connect(
            dbname='postgres', user='postgres.xzbozofttuvyijeimxkj',
            password='dnHmzMkSQhvMmCj8', host='aws-1-ap-south-1.pooler.supabase.com',
            port='6543', sslmode='require'
        )
        cur = conn.cursor()

        print("\n" + "="*50)
        print("🏛️  CODAC SOVEREIGN FOUNDER CONTROL PANEL")
        print("="*50)

        # 1. Personal Wallet Check
        cur.execute("SELECT reward_wallet, codac_coin_wallet FROM portal_citizens WHERE binary_id = 386;")
        wallet = cur.fetchone()
        
        if wallet:
            print(f"💰 PERSONAL REWARDS : {wallet[0]:,} USDT")
            print(f"🪙 CODAC COINS       : {wallet[1]:,} CODAC")
        else:
            print("⚠️ WALLET: Genesis Record (ID 386) not found in portal_citizens.")

        # 2. System-Wide Treasury Check
        cur.execute("SELECT SUM(treasury_balance), SUM(reserve_balance) FROM system_ledgers;")
        ledgers = cur.fetchone()
        
        if ledgers and ledgers[0] is not None:
            print(f"🏦 TOTAL TREASURY  : {ledgers[0]:,.2f} USDT")
            print(f"🛡️ SYSTEM RESERVE   : {ledgers[1]:,.2f} USDT")
        else:
            print("⚠️ LEDGER: No records found in system_ledgers yet.")

        # 3. Overall Progress
        cur.execute("SELECT COUNT(*) FROM portal_citizens;")
        total_pop = cur.fetchone()[0]
        print(f"🌳 TREE POPULATION  : {total_pop:,} / 1,048,576")

        print("="*50)
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ System Message: {e}")

if __name__ == "__main__":
    show_founder_stats()
