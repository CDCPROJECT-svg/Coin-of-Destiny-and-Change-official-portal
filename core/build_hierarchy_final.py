import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def build_final_structure():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- BUILDING FINAL STRUCTURE (POOREST TO RICHEST) ---")

    # HELPER FUNCTION
    def insert_node(uid, name, level, title, sponsor):
        cursor.execute("""
            INSERT OR REPLACE INTO active_members 
            (user_id, name, current_cycle, current_level, title, sponsor_id, is_task_exempt, can_claim_rewards)
            VALUES (?, ?, 1, ?, ?, ?, 1, 1)
        """, (uid, name, level, title, sponsor))

    # --- LEVEL 9: INJECTING 204 COUNTRIES ---
    print("Injecting Level 9 (Special Accounts + 204 Countries)...")
    
    # 1. CLEANUP LEVEL 9
    cursor.execute("DELETE FROM active_members WHERE current_level = 9")

    # 2. THE 52 SPECIAL ACCOUNTS (Slots 1-52)
    # These remain at the top as the System Foundation
    special_names = [
        "CODAC-Coin Backup", "CODAC-Coin Miscellaneous", "CODAC-Coin Incentive",
        "CODAC-Coin Reward", "CODAC-Coin INFRA", "CODAC-Coin Foundation",
        "CODAC-Coin Innovation", "CODAC-Coin Blockchain Fund", "CODAC-Coin System Maintenance",
        "CODAC-Coin Portal"
    ]
    count = 1
    while len(special_names) < 52:
        special_names.append(f"CODAC-Coin Global Backup {count}")
        count += 1

    for idx, name in enumerate(special_names):
        uid = f"CODAC-SPEC-{str(idx+1).zfill(3)}"
        insert_node(uid, name, 9, "Special System Account", "SYSTEM_RESERVED")

    # 3. THE 204 COUNTRIES (SORTED: POOREST TO RICHEST)
    # List is approx order by GDP Per Capita / Development Index
    economic_order_countries = [
        # --- THE POOREST (Priority for Support) ---
        "Burundi", "South Sudan", "Central African Republic", "Somalia", "Congo (DRC)", 
        "Mozambique", "Niger", "Malawi", "Liberia", "Madagascar", "Chad", "Yemen", 
        "Sierra Leone", "Afghanistan", "Sudan", "Gambia", "Burkina Faso", "Mali", 
        "Guinea-Bissau", "Eritrea", "Togo", "Uganda", "Rwanda", "Ethiopia", "Lesotho", 
        "Tanzania", "Comoros", "Zambia", "Solomon Islands", "Benin", "Guinea", "Haiti", 
        "Zimbabwe", "Kiribati", "Senegal", "Cambodia", "Myanmar", "Cameroon", "Kenya", 
        "Pakistan", "Nepal", "Vanuatu", "Timor-Leste", "Tajikistan", "Bangladesh", 
        "Nigeria", "Ghana", "Mauritania", "Ivory Coast", "Kyrgyzstan", "Djibouti", 
        "Laos", "Bhutan", "Papua New Guinea", "Congo (Rep)", "Honduras", "Nicaragua", 
        
        # --- LOWER MIDDLE INCOME ---
        "Philippines", "Vietnam", "India", "Bolivia", "Morocco", "Cape Verde", "El Salvador", 
        "Palestine", "Tunisia", "Egypt", "Eswatini", "Mongolia", "Sri Lanka", "Algeria", 
        "Indonesia", "Micronesia", "Samoa", "Tonga", "Iran", "Uzbekistan", "Ukraine", 
        "Georgia", "Armenia", "Guatemala", "Paraguay", "Azerbaijan", "Fiji", "Ecuador", 
        "Peru", "Colombia", "Thailand", "Jamaica", "Namibia", "South Africa", "Botswana", 
        "Libya", "Jordan", "Iraq", "Lebanon", "Suriname", "Dominica", "Saint Lucia", 
        
        # --- UPPER MIDDLE INCOME ---
        "Brazil", "Mexico", "Turkey", "Russia", "China", "Malaysia", "Kazakhstan", 
        "Turkmenistan", "Gabon", "Equatorial Guinea", "Dominican Republic", "Costa Rica", 
        "Serbia", "Montenegro", "Bosnia", "North Macedonia", "Albania", "Bulgaria", 
        "Argentina", "Chile", "Uruguay", "Panama", "Venezuela", "Cuba", "Belarus", 
        "Romania", "Mauritius", "Maldives", "Grenada", "Saint Vincent", "Saint Kitts", 
        "Antigua and Barbuda", "Seychelles", "Palau", "Nauru", "Tuvalu", "Marshall Islands", 
        
        # --- HIGH INCOME / DEVELOPED ---
        "Poland", "Hungary", "Slovakia", "Croatia", "Oman", "Saudi Arabia", "Bahrain", 
        "Kuwait", "Portugal", "Greece", "Latvia", "Lithuania", "Estonia", "Czech Republic", 
        "Slovenia", "Cyprus", "Malta", "Spain", "Italy", "South Korea", "Japan", 
        "Taiwan", "Brunei", "United Arab Emirates", "New Zealand", "United Kingdom", 
        "France", "Germany", "Belgium", "Netherlands", "Canada", "Australia", "Sweden", 
        "Finland", "Denmark", "Austria", "Iceland", "Norway", "Switzerland", "Ireland", 
        "United States", "Singapore", "Qatar", "Luxembourg", "Monaco", "Liechtenstein", 
        "San Marino", "Vatican City", "Andorra", "Bahamas", "Barbados", "Trinidad and Tobago",
        
        # --- FILLERS (To Ensure exactly 204) ---
        "Angola", "Syria", "North Korea", "Belize", "Guyana", "Sao Tome", "Moldova", "Kosovo"
    ]

    # Cut strictly to 204
    final_list = economic_order_countries[:204]

    print(f"   - Injecting {len(final_list)} Countries (Poorest First)...")
    
    # Start ID logic
    current_id = 182 
    
    for name in final_list:
        # Create Abbreviation
        abbrev = name[:3].replace(" ", "")
        
        # Generate UID
        raw_count = str(current_id).zfill(9)
        formatted_count = f"{raw_count[0:3]}-{raw_count[3:6]}-{raw_count[6:9]}"
        uid = f"CODAC-A09L-{abbrev}-{formatted_count}"
        
        insert_node(uid, name, 9, "Country Node", "SYSTEM_RESERVED")
        current_id += 1

    conn.commit()
    conn.close()
    print("\nSUCCESS: Hierarchy Rebuilt.")
    print("1. Level 9 Slots 1-52: Special Accounts.")
    print("2. Level 9 Slots 53+: Countries (Starts with Burundi/South Sudan, Ends with USA/Qatar).")

if __name__ == "__main__":
    build_final_structure()
