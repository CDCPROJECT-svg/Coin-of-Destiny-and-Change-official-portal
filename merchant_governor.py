import psycopg2
from datetime import datetime

def withdraw_merchant_funds(merchant_id, requested_amount):
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres.xzbozofttuvyijeimxkj',
            password='dnHmzMkSQhvMmCj8',
            host='aws-1-ap-south-1.pooler.supabase.com',
            port='6543',
            sslmode='require'
        )
        cur = conn.cursor()

        # 1. Fetch Merchant's Total Gross Sales and Last Withdrawal
        cur.execute("SELECT gross_sales_balance, last_withdrawal_date FROM merchants WHERE merchant_id = %s", (merchant_id,))
        gross_balance, last_date = cur.fetchone()

        # 2. Calculate the 8% Daily Limit
        daily_limit = float(gross_balance) * 0.08
        
        # 3. Check if they already withdrew today
        if last_date == datetime.now().date():
            print("❌ Error: Daily withdrawal limit already reached.")
            return

        # 4. Process withdrawal if within 8%
        if requested_amount <= daily_limit:
            new_balance = float(gross_balance) - requested_amount
            cur.execute("""
                UPDATE merchants 
                SET gross_sales_balance = %s, last_withdrawal_date = CURRENT_DATE 
                WHERE merchant_id = %s
            """, (new_balance, merchant_id))
            print(f"✅ Approved: {requested_amount} USDT released. (8% limit was {daily_limit})")
        else:
            print(f"❌ Denied: Requested amount exceeds 8% daily limit ({daily_limit}).")

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Merchant Logic Error: {e}")

if __name__ == "__main__":
    # Test for an affiliate merchant
    withdraw_merchant_funds("M_SHOP_001", 1000.00)
