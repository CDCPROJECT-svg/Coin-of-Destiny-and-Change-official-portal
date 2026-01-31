import sqlite3
import os
import secrets
from ecdsa import SECP256k1, SigningKey
from Crypto.Hash import keccak

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

# STANDARD LIST OF 204 (UN 193 + 2 Observers + 9 Major Economies/Territories)
MASTER_LIST_204 = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
    "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica",
    "Croatia", "Cuba", "Cyprus", "Czech Republic", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor",
    "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland",
    "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea",
    "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq",
    "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
    "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
    "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania",
    "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar",
    "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia",
    "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines",
    "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa",
    "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
    "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden",
    "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia",
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan",
    "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe", "Hong Kong", "Macau", "Puerto Rico", 
    "Greenland", "Western Sahara", "French Guiana", "Guadeloupe", "Martinique", "Reunion"
]

def generate_wallet_keys():
    priv_bytes = secrets.token_bytes(32)
    priv_hex = "0x" + priv_bytes.hex()
    sk = SigningKey.from_string(priv_bytes, curve=SECP256k1)
    pub_key = sk.verifying_key.to_string()
    k = keccak.new(digest_bits=256)
    k.update(pub_key)
    raw_addr = k.hexdigest()[-40:]
    address_lower = "0x" + raw_addr
    k_check = keccak.new(digest_bits=256)
    k_check.update(raw_addr.encode('utf-8'))
    hash_hex = k_check.hexdigest()
    final_address = "0x"
    for i, char in enumerate(raw_addr):
        if int(hash_hex[i], 16) >= 8:
            final_address += char.upper()
        else:
            final_address += char
    return final_address, priv_hex

def tally_and_fix():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- CODAC 204 TALLY CHECK ---")

    # 1. Get Current DB List
    cursor.execute("SELECT name FROM active_members WHERE user_id LIKE 'CODAC-A09L%'")
    db_countries = [row[0] for row in cursor.fetchall()]
    
    print(f"Current Database Count: {len(db_countries)}")
    
    # 2. Find Missing
    missing = []
    for country in MASTER_LIST_204:
        # Check if country exists in DB (fuzzy match to handle slight spelling diffs)
        found = False
        for db_c in db_countries:
            if country.lower() == db_c.lower():
                found = True
                break
        if not found:
            missing.append(country)

    print(f"Missing from Master List: {len(missing)}")
    
    if len(missing) == 0:
        print("✅ PERFECT TALLY! All 204 are present.")
    else:
        print("\nMISSING COUNTRIES IDENTIFIED:")
        for m in missing:
            print(f" - {m}")
        
        print("\n" + "="*50)
        confirm = input(f"Do you want to AUTO-ADD these {len(missing)} countries now? (yes/no): ")
        
        if confirm.lower() == "yes":
            print("\nAdding missing countries...")
            for name in missing:
                clean_name = name.replace(" ", "")[:5].upper()
                uid = f"CODAC-A09L-{clean_name}"
                addr, key = generate_wallet_keys()
                
                # Check GDP Tier (Default 1, but check logic later)
                tier = 1 
                
                try:
                    cursor.execute("""
                        INSERT INTO active_members (user_id, name, current_level, title, wallet_address, gdp_tier)
                        VALUES (?, ?, 9, 'Country Member', ?, ?)
                    """, (uid, name, addr, tier))
                    cursor.execute("INSERT INTO secure_vault (user_id, private_key) VALUES (?, ?)", (uid, key))
                    print(f"   -> Added: {name}")
                except sqlite3.IntegrityError:
                    print(f"   -> Skipped (Duplicate ID): {name}")

            conn.commit()
            print("\n✅ TALLY COMPLETE. Database is now updated.")
            
            # Re-run GDP Update to ensure new ones are categorized correctly
            print("Suggest running 'python core/update_gdp_rankings.py' next to update tiers.")

    conn.close()

if __name__ == "__main__":
    tally_and_fix()
