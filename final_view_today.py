import sqlite3
import os

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def audit():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="")
    print("=====================================================")
    print("      🔍 CODAC PROJECT PROGRESS AUDIT (TODAY)")
    print("=====================================================")
    
    # 1. Check Collector
    cur.execute("SELECT trading_points FROM active_members WHERE user_id = 'COLLECTOR-001'")
    coll_bal = cur.fetchone()[0]
    print(f" 🏦 COLLECTOR STATUS:  {coll_bal:,.4f} CODAC (Received Fee)")

    # 2. Check Founder/User Status
    cur.execute("SELECT current_cycle, locked_balance, lock_end_date FROM active_members WHERE user_id = 'FOUNDER-001'")
    cycle, lock, end_date = cur.fetchone()
    print(f" 👤 USER CYCLE:       CYCLE {cycle}")
    print(f" 🔒 CURRENT LOCK:     {lock:,.2f} CODAC")
    print(f" 📅 UNLOCK DATE:      {end_date}")
    
    print("-----------------------------------------------------")
    print(" ✅ UPDATED SCRIPTS:")
    print(" 1. member_login.py    - Internal Engine (No Permission Error)")
    print(" 2. milestone_table.py - Fixed Table & Universal 8-Year Rule")
    print(" 3. claim_milestone.py - Strict 8-Year Mandatory Lock")
    print(" 4. cycle_upgrade.py   - Diminishing Lock (.25 current)")
    print("=====================================================")
    
    conn.close()

if __name__ == "__main__":
    audit()
