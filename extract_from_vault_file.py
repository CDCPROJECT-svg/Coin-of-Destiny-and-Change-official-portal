import re
import csv
import os

# INPUT: Ang Master Vault na pinagkakatiwalaan mo
VAULT_PATH = "/sdcard/Download/CODAC_MASTER_VAULT_FINAL.txt"
# OUTPUT: Ang Final Clean List
EXPORT_FILE = "/sdcard/Download/CODAC_COUNTRIES_FROM_VAULT.csv"

def process_vault():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🔐 EXTRACTING FROM MASTER VAULT (READ-ONLY)")
    print("=========================================================")

    if not os.path.exists(VAULT_PATH):
        print(f"❌ ERROR: Vault file not found at {VAULT_PATH}")
        print("   Please generate the Master Vault first.")
        return

    print("   📖 Reading Master Vault file...")
    
    entries = []
    current_entry = {}
    
    # 1. READ THE TEXT FILE LINE BY LINE
    with open(VAULT_PATH, "r") as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        
        if line.startswith("NAME:"):
            current_entry["name"] = line.replace("NAME:", "").strip()
        elif line.startswith("ADDR:"):
            current_entry["addr"] = line.replace("ADDR:", "").strip()
        elif line.startswith("KEY:"):
            current_entry["key"] = line.replace("KEY:", "").strip()
        elif line.startswith("----------------"):
            # End of an entry, save it if complete
            if "name" in current_entry and "addr" in current_entry:
                name = current_entry["name"]
                # FILTER: Exclude System Accounts & Projects
                if not name.startswith("PROJ") and not name.startswith("CYCLE") and "FOUNDER" not in name and "RESERVE" not in name:
                    entries.append(current_entry)
            current_entry = {} # Reset

    # Sort Alphabetically
    entries.sort(key=lambda x: x["name"])
    
    # Remove Duplicates (Keep first occurrence)
    unique_entries = []
    seen_names = set()
    for e in entries:
        if e["name"] not in seen_names:
            unique_entries.append(e)
            seen_names.add(e["name"])

    print(f"   📊 Found {len(unique_entries)} Unique Countries in Vault.")
    print("   🏷️  Applying Format: CODAC-A09L-Code-000-000-Seq")

    # 2. WRITE TO CSV WITH NEW ID FORMAT
    with open(EXPORT_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "COUNTRY_NAME", "WALLET_ADDRESS", "PRIVATE_KEY"])
        
        count = 1
        for e in unique_entries:
            name = e["name"]
            
            # Format Code
            clean_name = name.replace(" ", "")
            code = clean_name[:3].capitalize()
            if name == "Austria": code = "Aut" # Fix conflict
            
            # Sequence
            seq = f"{count:03d}"
            
            # ID
            new_id = f"CODAC-A09L-{code}-000-000-{seq}"
            
            writer.writerow([new_id, name, e["addr"], e["key"]])
            count += 1

    print("-" * 57)
    print(f"   ✅ SUCCESS! Extracted cleanly from Vault.")
    print(f"   📂 File: CODAC_COUNTRIES_FROM_VAULT.csv")
    print(f"   📍 Check Downloads folder.")
    print("=========================================================")

if __name__ == "__main__":
    process_vault()
