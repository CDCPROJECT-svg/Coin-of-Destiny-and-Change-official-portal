import sqlite3
import os

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
# Siguraduhin na sa Downloads mapupunta
EXPORT_FILE = "/data/data/com.termux/files/home/storage/downloads/CODAC_FINAL_COMPLETED.txt"

def export_final():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print(f"   📄 WRITING TO: {EXPORT_FILE}...")
    
    try:
        with open(EXPORT_FILE, "w") as f:
            f.write("================================================================\n")
            f.write("   CODAC MASTER VAULT - FINAL COMPLETE VERSION\n")
            f.write("================================================================\n\n")
            
            # Select Founder first, then others
            cur.execute("SELECT user_id, name, wallet_address, private_key FROM active_members ORDER BY user_id")
            rows = cur.fetchall()
            
            for row in rows:
                uid, name, wallet, pkey = row
                
                # Default values if empty
                final_key = pkey if pkey else "MISSING"
                final_wallet = wallet if wallet else "MISSING"
                
                f.write(f"ID: {uid}\n")
                f.write(f"NAME: {name}\n")
                f.write(f"WALLET: {final_wallet}\n")
                f.write(f"PRIV KEY: {final_key}\n")
                f.write("-" * 60 + "\n")
                
        print("   ✅ SUCCESS! Check your Downloads folder now.")
        print(f"   📂 File Name: CODAC_FINAL_COMPLETED.txt")
        
    except Exception as e:
        print(f"   ❌ ERROR WRITING FILE: {e}")
        print("   Make sure Termux has storage permission (termux-setup-storage)")

if __name__ == "__main__":
    export_final()
