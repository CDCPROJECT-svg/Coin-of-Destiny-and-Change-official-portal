import csv
import os

# FILES
VAULT_PATH = "/sdcard/Download/CODAC_MASTER_VAULT_FINAL.txt"
EXPORT_FILE = "/sdcard/Download/CODAC_OFFICIAL_204_CLEAN.csv"

# THE OFFICIAL "STRICT" LIST (Only these names will be accepted)
TARGET_COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", 
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", 
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", 
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", 
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", 
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", 
    "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", 
    "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", 
    "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", 
    "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", 
    "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", 
    "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", 
    "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", 
    "Kazakhstan", "Kenya", "Kiribati", "North Korea", "South Korea", "Kosovo", "Kuwait", 
    "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", 
    "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", 
    "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", 
    "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", 
    "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", 
    "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", 
    "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", 
    "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", 
    "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", 
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", 
    "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", 
    "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", 
    "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", 
    "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", 
    "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", 
    "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", 
    "Yemen", "Zambia", "Zimbabwe"
]

def clean_filter():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🧹 STRICT FILTERING: REMOVING NON-COUNTRIES")
    print("=========================================================")

    if not os.path.exists(VAULT_PATH):
        print("❌ Vault file not found.")
        return

    # 1. Read Vault
    print("   📖 Scanning Vault for matches...")
    vault_data = {} # Name -> {addr, key}
    
    with open(VAULT_PATH, "r") as f:
        lines = f.readlines()
    
    current_name = None
    current_addr = None
    current_key = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("NAME:"): current_name = line.replace("NAME:", "").strip()
        elif line.startswith("ADDR:"): current_addr = line.replace("ADDR:", "").strip()
        elif line.startswith("KEY:"): current_key = line.replace("KEY:", "").strip()
        elif line.startswith("----------------"):
            if current_name and current_addr and current_key:
                # SAVE ONLY IF VALID
                vault_data[current_name] = {"addr": current_addr, "key": current_key}
            current_name = None

    # 2. Match with Strict List
    clean_entries = []
    
    print("   🔍 Matching against Official 204 List...")
    
    for country in TARGET_COUNTRIES:
        # Check Exact Match
        if country in vault_data:
            data = vault_data[country]
            clean_entries.append((country, data["addr"], data["key"]))
        else:
            # Check Partial Match (e.g. Vault has "Republic of Yemen" vs "Yemen")
            # Scan keys in vault
            found = False
            for v_name in vault_data:
                if country.lower() in v_name.lower():
                    data = vault_data[v_name]
                    clean_entries.append((country, data["addr"], data["key"]))
                    found = True
                    break
            
            # If still missing, report it
            # if not found: print(f"      ⚠️ Missing: {country}")

    # Remove duplicates if any
    clean_entries = sorted(list(set(clean_entries)), key=lambda x: x[0])

    print(f"   📊 Final Count: {len(clean_entries)} Official Countries.")

    # 3. Write CSV with Format
    with open(EXPORT_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "COUNTRY_NAME", "WALLET_ADDRESS", "PRIVATE_KEY"])
        
        count = 1
        for item in clean_entries:
            name, addr, key = item
            
            # ID Format
            clean_name = name.replace(" ", "")
            code = clean_name[:3].capitalize()
            if name == "Austria": code = "Aut"
            seq = f"{count:03d}"
            
            new_id = f"CODAC-A09L-{code}-000-000-{seq}"
            
            writer.writerow([new_id, name, addr, key])
            count += 1

    print("-" * 57)
    print(f"   ✅ SUCCESS! Cleaned list saved.")
    print(f"   📂 File: CODAC_OFFICIAL_204_CLEAN.csv")
    print(f"   📍 Check Downloads folder.")
    print("=========================================================")

if __name__ == "__main__":
    clean_filter()
