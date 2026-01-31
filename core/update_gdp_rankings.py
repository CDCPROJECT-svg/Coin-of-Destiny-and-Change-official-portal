import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

# LIST OF 86 RICHER/DEVELOPED/EMERGING ECONOMIES (High GDP)
# These will be Group B. The rest (118) will be Group A (Poorest).
RICH_LIST = [
    "United States", "China", "Japan", "Germany", "India", "United Kingdom", "France", "Italy", "Brazil", "Canada",
    "Russia", "South Korea", "Australia", "Mexico", "Spain", "Indonesia", "Saudi Arabia", "Netherlands", "Turkey", "Switzerland",
    "Poland", "Sweden", "Belgium", "Thailand", "Ireland", "Argentina", "Norway", "Israel", "Austria", "Nigeria",
    "United Arab Emirates", "Egypt", "Philippines", "Vietnam", "Malaysia", "South Africa", "Bangladesh", "Denmark", "Singapore", "Hong Kong",
    "Colombia", "Pakistan", "Chile", "Finland", "Romania", "Czech Republic", "Portugal", "New Zealand", "Peru", "Greece",
    "Iraq", "Kazakhstan", "Hungary", "Qatar", "Algeria", "Kuwait", "Morocco", "Slovakia", "Ecuador", "Puerto Rico",
    "Kenya", "Angola", "Dominican Republic", "Ethiopia", "Oman", "Guatemala", "Bulgaria", "Luxembourg", "Sri Lanka", "Tanzania",
    "Turkmenistan", "Azerbaijan", "Panama", "Ivory Coast", "Costa Rica", "Lithuania", "Croatia", "Uruguay", "Serbia", "Uzbekistan",
    "Slovenia", "Belarus", "Congo", "Venezuela", "Myanmar"
]
# Note: This logic ensures we separate the Top 86 from the Bottom 118 based on general GDP data.

def update_gdp_logic():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- UPDATING SYSTEM WITH GDP INTELLIGENCE ---")

    # 1. Add GDP Column if not exists
    try:
        cursor.execute("ALTER TABLE active_members ADD COLUMN gdp_tier INTEGER DEFAULT 1")
        print("✅ Added 'gdp_tier' column to database.")
    except sqlite3.OperationalError:
        print("ℹ️ 'gdp_tier' column already exists.")

    # 2. Reset all to Tier 1 (Poorest/Default)
    cursor.execute("UPDATE active_members SET gdp_tier = 1 WHERE user_id LIKE 'CODAC-A09L%'")
    
    # 3. Detect and Update Tier 2 (Richest 86)
    count_rich = 0
    
    # Get all countries
    cursor.execute("SELECT user_id, name FROM active_members WHERE user_id LIKE 'CODAC-A09L%'")
    all_countries = cursor.fetchall()
    
    for uid, name in all_countries:
        # Check if country name is in our Rich List (Case insensitive match)
        is_rich = False
        for rich_name in RICH_LIST:
            if rich_name.lower() in name.lower() or rich_name.lower() in uid.lower():
                is_rich = True
                break
        
        if is_rich:
            cursor.execute("UPDATE active_members SET gdp_tier = 2 WHERE user_id = ?", (uid,))
            count_rich += 1
            # print(f"   -> Detected Economy: {name} (Tier 2)")

    conn.commit()
    conn.close()
    
    print("\nSUMMARY:")
    print(f"Total Countries Scanned: {len(all_countries)}")
    print(f"Detected Developed/Emerging (Group B): {count_rich} (Target ~86)")
    print(f"Detected Poorest/Developing (Group A): {len(all_countries) - count_rich} (Target ~118)")
    print("System is now ready to auto-detect based on GDP Tier.")

if __name__ == "__main__":
    update_gdp_logic()
