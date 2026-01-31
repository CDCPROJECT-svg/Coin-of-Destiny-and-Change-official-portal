import sqlite3
import datetime

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def claim_process():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\n=====================================================")
    print("   🏆 CODAC MILESTONE CLAIM: UNIVERSAL ACTIVATION")
    print("=====================================================")
    
    user_id = input("   👉 ENTER USER ID: ").strip().upper()
    cur.execute("SELECT name, is_milestone_claimed, trading_points, locked_balance FROM active_members WHERE user_id=?", (user_id,))
    row = cur.fetchone()

    if not row:
        print("   ❌ USER NOT FOUND."); conn.close(); return
    
    name, claimed, wallet, current_lock = row

    # Global Rule: Every new member's first claim triggers the 8-year lock
    if claimed == 1:
        print(f"   ⚠️  {name}, you have already completed your initial activation.")
        print("   Checking for next available milestone rewards...")
        # (Future logic for subsequent rewards would go here)
        conn.close(); return

    print(f"\n   👤 WELCOME NEW PIONEER: {name}")
    print("   📢 FIRST MILESTONE REWARD ACTIVATION")
    print("   -----------------------------------------------------")
    print("   📜 UNIVERSAL MANDATORY TERMS:")
    print("   ● INITIAL REWARD:   8.00 CODAC")
    print("   ● MANDATORY LOCK:  -1.00 CODAC (Security Bond)")
    print("   ● LOCK DURATION:    8 YEARS FIXED")
    print("   ● NET TO WALLET:    7.00 CODAC")
    print("   -----------------------------------------------------")
    print("   ⚠️ This lock is required for ALL new members to be")
    print("      eligible for Grand Rewards (Levels 1-17).")
    print("   -----------------------------------------------------")

    confirm = input("   Type 'ACCEPT' to secure your 8-year bond: ").strip().upper()
    
    if confirm == "ACCEPT":
        # Fixed 8 Years from current date
        unlock_date = (datetime.datetime.now() + datetime.timedelta(days=365*8)).strftime("%Y-%m-%d")
        
        cur.execute("""
            UPDATE active_members 
            SET trading_points = trading_points + 7.00,
                locked_balance = locked_balance + 1.00,
                lock_end_date = ?,
                is_milestone_claimed = 1,
                current_cycle = 1,
                status = 'ACTIVE'
            WHERE user_id = ?
        """, (unlock_date, user_id))
        
        conn.commit()
        print(f"\n   🚀 ACTIVATION SUCCESSFUL!")
        print(f"   📅 1.00 CODAC is locked until {unlock_date}.")
        print("   💰 7.00 CODAC added to your Main Wallet.")
    else:
        print("   ❌ Activation halted.")
    
    conn.close()

if __name__ == "__main__":
    claim_process()
