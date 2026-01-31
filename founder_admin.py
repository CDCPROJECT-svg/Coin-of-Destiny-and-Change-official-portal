import psycopg2
import getpass
import sys

# --- MASTER CONFIG ---
# This is stored in local memory for this script
MASTER_PWD = "CODAC_FOUNDER_2026"

# --- RECOVERY QUESTIONS ---
RECOVERY = {
    "Q1": "ano ang tawag ng nanay sa kanya",
    "A1": "Uday",
    "Q2": "ano ang sinabi ni nanay kay founder bago xa mamatay",
    "A2": "waray pa gastador nga nag riko",
    "Q3": "kilan namatay ang nanay ni founder",
    "A3": "Dec.11, 2020"
}

def recover_password():
    print("\n⚠️ FORGOT PASSWORD: Initiating Sovereign Recovery...")
    ans1 = input(f"Q1: {RECOVERY['Q1']}? ")
    ans2 = input(f"Q2: {RECOVERY['Q2']}? ")
    ans3 = input(f"Q3: {RECOVERY['Q3']}? ")

    if ans1 == RECOVERY['A1'] and ans2 == RECOVERY['A2'] and ans3 == RECOVERY['A3']:
        print(f"\n✅ RECOVERY SUCCESS. Your Master Password is: {MASTER_PWD}")
        return True
    else:
        print("\n❌ ACCESS DENIED: Security answers are incorrect.")
        return False

def admin_panel():
    global MASTER_PWD
    print("\n--- 🛡️ CODAC SOVEREIGN ADMIN PANEL ---")
    pwd = getpass.getpass("Enter Master Password (or type 'RESET'): ")
    
    if pwd == "RESET":
        if not recover_password():
            sys.exit()
        pwd = MASTER_PWD

    if pwd != MASTER_PWD:
        print("❌ ACCESS DENIED: Invalid Password.")
        sys.exit()
        
    print("✅ ACCESS GRANTED. Welcome, Founder.")
    
    while True:
        print("\n[1] Add/Expand YouTube Channels")
        print("[2] Change Master Password")
        print("[3] Exit")
        choice = input("\nSelect Option: ")

        if choice == "1":
            name = input("Channel Name: ")
            url = input("YouTube URL: ")
            # Database logic for adding channel
            print(f"✅ Channel '{name}' added.")
            
        elif choice == "2":
            new_pwd = input("Enter New Master Password: ")
            confirm = input("Confirm New Password: ")
            if new_pwd == confirm:
                MASTER_PWD = new_pwd
                print("✅ Password updated successfully.")
            else:
                print("❌ Passwords do not match.")
                
        elif choice == "3":
            print("Closing Session. Hayahay!")
            break

if __name__ == "__main__":
    admin_panel()
