import os
import shutil

def setup_clean_vault():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🛡️  CREATING CLEAN OFFICIAL VAULT")
    print("=========================================================")
    
    # 1. Create the new clean directory
    clean_dir = os.path.expanduser("~/CODAC_OFFICIAL_CLEAN")
    if not os.path.exists(clean_dir):
        os.makedirs(clean_dir)
        print(f"   ✅ Folder Created: {clean_dir}")

    # 2. Path to your current database files
    # Binabase natin ito sa 'database' folder na nakita natin sa 'ls' kanina
    db_source = os.path.expanduser("~/codac-coin_portal/database")
    
    if os.path.exists(db_source):
        print(f"   📦 Copying clean files from database folder...")
        # Kopyahin lang ang mga scripts (.py) para manatiling malinis
        for item in os.listdir(db_source):
            if item.endswith('.py') or item.endswith('.sh'):
                shutil.copy2(os.path.join(db_source, item), clean_dir)
        print("   ✅ Scripts successfully moved to Clean Vault.")
    else:
        print("   ⚠️  Warning: 'database' folder not found. Manual check required.")

    print("=========================================================")
    print("   NEXT: I-check natin ang loob ng CODAC_OFFICIAL_CLEAN")
    print("=========================================================")

if __name__ == "__main__":
    setup_clean_vault()
