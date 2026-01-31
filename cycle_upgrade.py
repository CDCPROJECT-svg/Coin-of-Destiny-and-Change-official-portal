import sqlite3
import time
import datetime

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def clear():
    print("\033[H\033[J", end="")

def calculate_required_lock(cycle_number):
    # Cycle 1 = 1.0, Cycle 2 = 0.5, Cycle 3 = 0.25...
    return 1.0 * (0.5 ** (cycle_number - 1))

def upgrade_cycle():
    clear()
    print("=====================================================")
    print("   🔄 CODAC CYCLE TRANSITION PROTOCOL")
    print("=====================================================")
    
    user_id = input("   👉 ENTER USER ID TO UPGRADE: ").strip().upper()
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Get User Data
    cur.execute("SELECT name, current_cycle, trading_points, locked_balance FROM active_members WHERE user_id=?", (user_id,))
    row = cur.fetchone()

    if not row:
        print("   ❌ ERROR: User not found."); conn.close(); return

    name = row[0]
    current_cycle = row[1] if row[1] else 1
    wallet_bal = row[2]
    current_locked = row[3]

    next_cycle = current_cycle + 1
    required_lock = calculate_required_lock(next_cycle) # New lower lock
    prev_lock_fee = calculate_required_lock(current_cycle) # Fee to Collector

    print(f"\n   👤 MEMBER: {name}")
    print(f"   🔄 STATUS: CYCLE {current_cycle} -> CYCLE {next_cycle}")
    print("   -----------------------------------------------------")
    
    print(f"   🧾 SYSTEM FEE: {prev_lock_fee} CODAC (From Old Lock)")
    print(f"   📉 NEW REQUIREMENT: {required_lock} CODAC (50% Off)")
    
    if wallet_bal < required_lock:
        print(f"\n   ❌ INSUFFICIENT FUNDS IN WALLET.")
        print(f"   👉 You need {required_lock} CODAC to enter Cycle {next_cycle}.")
        conn.close(); return

    print("\n   ⏳ LOCK DURATION SETTINGS")
    try:
        years = int(input("   👉 Enter Lock Duration (3-18 Years): "))
        if years < 3 or years > 18:
            print("   ❌ ERROR: Must be between 3 and 18 years.")
            conn.close(); return
    except:
        print("   ❌ ERROR: Invalid number.")
        conn.close(); return

    print("\n   ⚠️  CONFIRM CYCLE UPGRADE:")
    print(f"   1. {prev_lock_fee} CODAC -> Sent to COLLECTOR-001")
    print(f"   2. {required_lock} CODAC -> LOCKED for {years} Years")
    
    confirm = input("\n   Type 'PROCEED' to execute: ").strip().upper()

    if confirm == "PROCEED":
        # 1. Collector takes the old lock amount
        cur.execute("UPDATE active_members SET trading_points = trading_points + ? WHERE user_id='COLLECTOR-001'", (prev_lock_fee,))
        
        # 2. Update User (Deduct Wallet, Set New Lock)
        new_wallet_bal = wallet_bal - required_lock
        
        # Calculate Logic: Old Lock is gone (paid as fee), New Lock comes from Wallet
        final_locked_bal = required_lock 

        future_date = datetime.datetime.now() + datetime.timedelta(days=365 * years)
        unlock_date = future_date.strftime("%Y-%m-%d")

        cur.execute("""
            UPDATE active_members 
            SET current_cycle = ?,
                trading_points = ?,
                locked_balance = ?,
                lock_end_date = ?
            WHERE user_id = ?
        """, (next_cycle, new_wallet_bal, final_locked_bal, unlock_date, user_id))

        conn.commit()
        print(f"\n   🚀 SUCCESS! UPGRADED TO CYCLE {next_cycle}")
        print(f"   🔒 New Locked Amount: {final_locked_bal:.4f} CODAC")
        
    else:
        print("   ❌ CANCELLED.")

    conn.close()

if __name__ == "__main__":
    upgrade_cycle()
