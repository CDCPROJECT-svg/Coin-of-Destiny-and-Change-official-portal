import os

# FOLDER
DOWNLOAD_DIR = "/sdcard/Download/"

# ANG MGA DAPAT MATIRA (DO NOT TOUCH)
KEEP_SAFE = [
    "CODAC_MASTER_VAULT_FINAL.pdf",  # Ang Bible (Complete)
    "CODAC_MASTER_VAULT_FINAL.txt",  # Ang Text Version
    "CODAC_OFFICIAL_204_FINAL.csv"   # Ang Final 204 List
]

def scan_only():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      👁️  PREVIEW: LIST OF FILES TO BE DELETED")
    print("      (Note: Nothing will be deleted yet. View only.)")
    print("=========================================================")

    all_files = os.listdir(DOWNLOAD_DIR)
    
    found_trash = 0
    found_safe = 0
    personal_files = 0

    print("   📂 FILES IN YOUR DOWNLOAD FOLDER:\n")

    for filename in sorted(all_files):
        # 1. Check kung CODAC CSV ba siya
        if filename.startswith("CODAC_") and filename.endswith(".csv"):
            
            # Check kung PROTECTED
            if filename in KEEP_SAFE:
                print(f"      ✅  KEEP (SAFE):     {filename}")
                found_safe += 1
            else:
                # Ito ang mga Candidates for Deletion
                print(f"      ❌  TO DELETE:       {filename}")
                found_trash += 1
        
        # 2. Check kung Master Vault (PDF/TXT)
        elif filename.startswith("CODAC_MASTER_VAULT"):
             print(f"      ✅  KEEP (VAULT):    {filename}")
             found_safe += 1

        # 3. Ibang Files (Personal, Pictures, etc.)
        else:
            # Hindi natin ililista isa-isa para di mahaba, pero bilangin natin
            personal_files += 1

    print("\n" + "-" * 57)
    print(f"   📊 SUMMARY:")
    print(f"      ✅  Files na ILILIGTAS:   {found_safe} (Vaults & Official 204)")
    print(f"      ❌  Files na BUBURAHIN:   {found_trash} (Lumang CSV/Trials)")
    print(f"      🛡️  Personal Files:       {personal_files} (Ligtas/Ignored)")
    print("=========================================================")

if __name__ == "__main__":
    scan_only()
