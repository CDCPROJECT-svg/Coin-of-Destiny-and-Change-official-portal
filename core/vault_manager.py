import sqlite3
import os
import csv
import sys

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def vault_manager():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n--- CODAC SECURE VAULT MANAGER ---")
    print("WARNING: You are accessing sensitive Private Keys.")
    print("1. View Private Key for ONE Account")
    print("2. EXPORT ALL Keys to CSV (Encrypted Backup)")
    
    choice = input("\nEnter Choice (1 or 2): ")

    if choice == "1":
        target_id = input("Enter User ID (e.g., FOUNDER-001): ").strip()
        
        query = """
            SELECT m.user_id, m.name, m.wallet_address, v.private_key 
            FROM active_members m
            JOIN secure_vault v ON m.user_id = v.user_id
            WHERE m.user_id = ?
        """
        cursor.execute(query, (target_id,))
        row = cursor.fetchone()
        
        if row:
            print("\n" + "="*60)
            print(f"ACCOUNT: {row[1]} ({row[0]})")
            print(f"ADDRESS: {row[2]}")
            print("-" * 60)
            print(f"PRIVATE KEY: {row[3]}")
            print("="*60)
            print("Copy this key and import to Metamask.")
        else:
            print("Error: Account not found or no key generated.")

    elif choice == "2":
        confirm = input("This will save ALL 503 keys to a file. Continue? (yes/no): ")
        if confirm.lower() == "yes":
            outfile = "codac_full_backup.csv"
            
            cursor.execute("""
                SELECT m.user_id, m.name, m.wallet_address, v.private_key 
                FROM active_members m
                JOIN secure_vault v ON m.user_id = v.user_id
                ORDER BY m.current_level, m.user_id
            """)
            rows = cursor.fetchall()
            
            with open(outfile, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["User ID", "Name", "Public Address", "Private Key"])
                writer.writerows(rows)
                
            print(f"\nSUCCESS: Exported {len(rows)} keys to '{outfile}'.")
            print(f"To move to downloads: cp {outfile} /sdcard/Download/")
            print("KEEP THIS FILE SAFE! DELETE AFTER TRANSFERRING.")
        else:
            print("Export cancelled.")

    conn.close()

if __name__ == "__main__":
    vault_manager()
