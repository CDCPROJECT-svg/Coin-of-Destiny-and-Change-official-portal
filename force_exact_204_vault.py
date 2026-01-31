import csv
import os

# FILES
VAULT_PATH = "/sdcard/Download/CODAC_MASTER_VAULT_FINAL.txt"
EXPORT_FILE = "/sdcard/Download/CODAC_OFFICIAL_204_FINAL.csv"

def force_204():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      ⚖️  BALANCING LIST TO EXACTLY 204 ENTRIES")
    print("=========================================================")

    if not os.path.exists(VAULT_PATH):
        print("❌ Vault file missing.")
        return

    # 1. READ ALL ENTRIES FROM VAULT
    raw_entries = []
    current_entry = {}
    
    with open(VAULT_PATH, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if line.startswith("NAME:"): current_entry["name"] = line.replace("NAME:", "").strip()
        elif line.startswith("ADDR:"): current_entry["addr"] = line.replace("ADDR:", "").strip()
        elif line.startswith("KEY:"): current_entry["key"] = line.replace("KEY:", "").strip()
        elif line.startswith("----------------"):
            if "name" in current_entry:
                raw_entries.append(current_entry)
            current_entry = {}

    print(f"   📖 Scanned {len(raw_entries)} total entries from Vault.")

    # 2. SMART FILTER (Remove Non-Countries)
    # We remove anything that looks like a System Account
    valid_countries = []
    
    blacklist = ["PROJ", "CYCLE", "TEAM", "DEPT", "MAIN", "RESERVE", "FOUNDER", "SYSTEM", "BANK"]
    
    for entry in raw_entries:
        name = entry["name"]
        
        # Check if name contains any blacklist keyword
        is_system = False
        for word in blacklist:
            if word in name.upper(): # Check Case Insensitive
                is_system = True
                break
        
        if not is_system:
            valid_countries.append(entry)

    # 3. REMOVE DUPLICATES & SORT
    # Use a dictionary to keep unique names only
    unique_map = {e["name"]: e for e in valid_countries}
    sorted_countries = sorted(unique_map.values(), key=lambda x: x["name"])
    
    current_count = len(sorted_countries)
    print(f"   🔍 Found {current_count} Valid Candidates (Non-System).")

    # 4. CUT OR FILL TO 204
    final_list = []
    
    if current_count >= 204:
        print("   ✂️  Trimming list to exactly 204...")
        final_list = sorted_countries[:204]
    else:
        print(f"   ⚠️  Warning: Only found {current_count}. Saving all of them.")
        final_list = sorted_countries

    # 5. EXPORT WITH FORMAT
    print("   🏷️  Applying Format: CODAC-A09L-Code-000-000-Seq")
    
    with open(EXPORT_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "COUNTRY_NAME", "WALLET_ADDRESS", "PRIVATE_KEY"])
        
        count = 1
        for item in final_list:
            name = item["name"]
            addr = item["addr"]
            key = item["key"]
            
            # Code
            clean_name = name.replace(" ", "")
            code = clean_name[:3].capitalize()
            if name == "Austria": code = "Aut"
            
            seq = f"{count:03d}"
            new_id = f"CODAC-A09L-{code}-000-000-{seq}"
            
            writer.writerow([new_id, name, addr, key])
            count += 1

    print("-" * 57)
    print(f"   ✅ SUCCESS! Saved exactly {len(final_list)} entries.")
    print(f"   📂 File: CODAC_OFFICIAL_204_FINAL.csv")
    print(f"   📍 Location: Downloads Folder")
    
    # Verification
    if len(final_list) >= 1:
        print(f"\n   1. {final_list[0]['name']}")
    if len(final_list) >= 204:
        print(f"   204. {final_list[203]['name']}")

    print("=========================================================")

if __name__ == "__main__":
    force_204()
