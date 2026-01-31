import os

# PATHS
DOWNLOADS = "/sdcard/Download/"

# OLD NAMES (Yung nahanap mo)
old_csv = os.path.join(DOWNLOADS, "CODAC_204_COUNTRIES_RESCUED.csv")
old_txt = os.path.join(DOWNLOADS, "CODAC_BANKING_STRUCTURE_RESCUED.txt")

# NEW OFFICIAL NAMES (Ang gusto natin)
new_csv = os.path.join(DOWNLOADS, "CODAC_OFFICIAL_204_DEPLOYMENT.csv")
new_txt = os.path.join(DOWNLOADS, "CODAC_BANKING_STRUCTURE_OFFICIAL.txt")

def rename_files():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🏷️  FINALIZING FILE NAMES (OFFICIAL)")
    print("=========================================================")

    # 1. RENAME CSV (204 Countries)
    if os.path.exists(old_csv):
        os.rename(old_csv, new_csv)
        print(f"   ✅ RENAMED: CODAC_OFFICIAL_204_DEPLOYMENT.csv")
    elif os.path.exists(new_csv):
        print(f"   👌 ALREADY OFFICIAL: CODAC_OFFICIAL_204_DEPLOYMENT.csv")
    else:
        print("   ⚠️  CSV file not found to rename.")

    # 2. RENAME TXT (Banking Structure)
    if os.path.exists(old_txt):
        os.rename(old_txt, new_txt)
        print(f"   ✅ RENAMED: CODAC_BANKING_STRUCTURE_OFFICIAL.txt")
    elif os.path.exists(new_txt):
        print(f"   👌 ALREADY OFFICIAL: CODAC_BANKING_STRUCTURE_OFFICIAL.txt")
    else:
        print("   ⚠️  TXT file not found to rename.")

    print("-" * 57)
    print("   🚀 FILES ARE NOW READY AND CORRECTLY NAMED!")
    print("=========================================================")

if __name__ == "__main__":
    rename_files()
