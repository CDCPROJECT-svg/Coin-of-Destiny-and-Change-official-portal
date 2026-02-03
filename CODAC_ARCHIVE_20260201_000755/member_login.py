import sqlite3
import os
import time
import sys

# --- CONFIGURATION ---
DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
BASE_DIR = "/data/data/com.termux/files/home/codac-coin_portal"

def clear_screen():
    # Pure Python clear - No shell permissions needed
    print("\033[H\033[J", end="")

def internal_run(file_name):
    path = os.path.join(BASE_DIR, file_name)
    if os.path.exists(path):
        with open(path, "r") as f:
            code = f.read()
            # Execute with a clean global context but shared with current process
            exec(code, globals())
    else:
        print(f"\n   ❌ ERROR: {file_name} not found.")

def get_balance(cur, user_id, column="trading_points"):
    try:
        cur.execute(f"SELECT {column} FROM active_members WHERE user_id = ?", (user_id,))
        res = cur.fetchone()
        return res[0] if res else 0.00
    except:
        return 0.00

def display_dashboard(cur, user_id, name, join_date, level, status):
    my_coin  = get_balance(cur, user_id, "trading_points")
    my_lock  = get_balance(cur, user_id, "locked_balance")
    my_usdt  = get_balance(cur, user_id, "usdt_balance")

    print("=====================================================")
    print("          CODAC COIN OF DESTINY & CHANGE  ")
    print("=====================================================")
    print(f" ID: {user_id:<18} Join Date: {join_date}")
    print("-----------------------------------------------------")
    print(f" 🛡️  STATUS: {status}")
    print(f" 🔒 LOCKED ASSETS:    {my_lock:,.2f} CODAC")
    print("-----------------------------------------------------")
    print(" 👤 YOUR ACCOUNT WALLETS")
    print(f"   💰 CODAC COIN WALLET:      {my_coin:,.2f}")
    print(f"   💲 USDT WALLET:            {my_usdt:,.2f}")
    print("-----------------------------------------------------")
    
    target = 20
    filled = int((level / target) * 20)
    bar = "█" * filled + "░" * (20 - filled)
    print(f" LEVEL {level}/20: [{bar}]")
    print("=====================================================")
    print(" [C] CLAIM REWARDS   | [M] MILESTONE TABLE")
    print(" [U] CYCLE UPGRADE   | [X] EXIT")

def login():
    clear_screen()
    print("========================================================")
    print("   🔐 CODAC AUTHORITY PORTAL | INTERNAL ENGINE")
    print("========================================================")
    
    user_id = input("   👉 ENTER USER ID: ").strip().upper()
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT name, status, current_level, locked_balance, is_milestone_claimed FROM active_members WHERE user_id=?", (user_id,))
    row = cur.fetchone()

    if not row:
        print("\n   ❌ ACCESS DENIED."); conn.close(); return

    name, status_db, level, lock_bal, claimed = row
    lock_bal = lock_bal if lock_bal else 0.00

    while True:
        clear_screen()
        display_dashboard(cur, user_id, name, "04 Jan 2026", level, status_db)
        
        opt = input("\n   👉 COMMAND: ").strip().upper()
        
        if opt == 'C':
            internal_run("claim_milestone.py")
            input("\n   [PRESS ENTER TO RETURN]") 
        elif opt == 'M':
            internal_run("milestone_table.py")
            input("\n   [PRESS ENTER TO RETURN]") 
        elif opt == 'U':
            internal_run("cycle_upgrade.py")
            input("\n   [PRESS ENTER TO RETURN]")
        elif opt == 'X':
            print("   👋 LOGGING OUT..."); break
    conn.close()

if __name__ == "__main__":
    login()
