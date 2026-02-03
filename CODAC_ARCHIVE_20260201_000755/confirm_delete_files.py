import os

DOWNLOAD_DIR = "/sdcard/Download/"

# ITO LANG ANG BUBURAHIN (Kopyahin natin ang listahan ng basura)
TRASH_LIST = [
    "CODAC_204_COUNTRIES_BATCH.csv",
    "CODAC_ALL_COUNTRIES_FINAL_EXTRACT.csv",
    "CODAC_COUNTRIES_FROM_VAULT.csv",
    "CODAC_OFFICIAL_204_CLEAN.csv",
    "CODAC_OFFICIAL_204_COUNTRIES_COMPLETE.csv"
]

def delete_trash():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🗑️  EXECUTING DELETION (TRASH FILES ONLY)")
    print("=========================================================")

    deleted_count = 0

    for filename in TRASH_LIST:
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"      ❌ DELETED: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"      ⚠️  Error: {e}")
        else:
            print(f"      👌 Already gone: {filename}")

    print("-" * 57)
    print(f"   ✨ MALINIS NA! {deleted_count} files removed.")
    print("   ✅ Ang natira lang ay ang FINAL at OFFICIAL files.")
    print("=========================================================")

if __name__ == "__main__":
    delete_trash()
