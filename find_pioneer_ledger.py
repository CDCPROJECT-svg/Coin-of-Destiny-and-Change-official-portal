import os

def find_the_ledger():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🕵️ FILE HUNTER: OFFICIAL PIONEER RECORDS")
    print("=========================================================")

    # Keywords to search for
    keywords = ["PIONEER", "OFFICIAL", "LEDGER", "RECORDS"]
    found_files = []

    # Walk through all directories
    for root, dirs, files in os.walk("."):
        for file in files:
            # Check if file name matches the user's request
            if any(k in file.upper() for k in keywords):
                full_path = os.path.join(root, file)
                found_files.append(full_path)

    if found_files:
        print(f" [✅] FOUND {len(found_files)} MATCHING FILES:")
        for f in found_files:
            print(f"      📂 {f}")
            
        print("\n [?] Founder, alin sa mga ito ang gagamitin natin?")
        print("     (Kung PDF ito, kailangan natin ang .csv o .txt version nito)")
    else:
        print(" [❌] CRITICAL: File with name 'OFFICIAL PIONEER RECORDS' not found.")
        print("      Available 'LEDGER' files found:")
        # Fallback search for just 'LEDGER'
        for root, dirs, files in os.walk("."):
            for file in files:
                if "LEDGER" in file.upper():
                    print(f"      - {file}")

    print("=========================================================")

if __name__ == "__main__":
    find_the_ledger()
