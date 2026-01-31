import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

# Listahan ng 86 Countries (Developing to Richest) 
# Ito ang magsisilbing Group B. Ang hindi kasama dito ay automatic Group A (118 Poorest).
GROUP_B_TARGET = [
    "United States", "China", "Japan", "Germany", "India", "United Kingdom", "France", "Italy", "Brazil", "Canada",
    "Russia", "South Korea", "Australia", "Mexico", "Spain", "Indonesia", "Saudi Arabia", "Netherlands", "Turkey", "Switzerland",
    "Poland", "Sweden", "Belgium", "Thailand", "Ireland", "Argentina", "Norway", "Israel", "Austria", "United Arab Emirates",
    "Egypt", "Philippines", "Vietnam", "Malaysia", "South Africa", "Bangladesh", "Denmark", "Singapore", "Hong Kong", "Colombia",
    "Pakistan", "Chile", "Finland", "Romania", "Czech Republic", "Portugal", "New Zealand", "Peru", "Greece", "Iraq",
    "Kazakhstan", "Hungary", "Qatar", "Algeria", "Kuwait", "Morocco", "Slovakia", "Ecuador", "Puerto Rico", "Kenya",
    "Angola", "Dominican Republic", "Ethiopia", "Oman", "Guatemala", "Bulgaria", "Luxembourg", "Sri Lanka", "Tanzania", "Turkmenistan",
    "Azerbaijan", "Panama", "Ivory Coast", "Costa Rica", "Lithuania", "Croatia", "Uruguay", "Serbia", "Uzbekistan", "Slovenia",
    "Belarus", "Macau", "Bulgaria", "Jordan", "Tunisia", "Libya"
]

def apply_gdp():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Reset all to Group A (Tier 1)
    cursor.execute("UPDATE active_members SET gdp_tier = 1 WHERE user_id LIKE 'CODAC-A09L%'")
    
    # 2. Assign Group B (Tier 2)
    count_b = 0
    cursor.execute("SELECT user_id, name FROM active_members WHERE user_id LIKE 'CODAC-A09L%'")
    rows = cursor.fetchall()
    
    for uid, name in rows:
        if any(rich_n.lower() in name.lower() for rich_n in GROUP_B_TARGET):
            cursor.execute("UPDATE active_members SET gdp_tier = 2 WHERE user_id = ?", (uid,))
            count_b += 1

    conn.commit()
    
    # 3. Final Tally Check
    cursor.execute("SELECT count(*) FROM active_members WHERE user_id LIKE 'CODAC-A09L%' AND gdp_tier = 1")
    count_a = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM active_members WHERE user_id LIKE 'CODAC-A09L%' AND gdp_tier = 2")
    count_b = cursor.fetchone()[0]
    
    print(f"--- GDP TALLY COMPLETE ---")
    print(f"Group A (Poorest - 118 Target): {count_a}")
    print(f"Group B (Rich/Dev - 86 Target): {count_b}")
    conn.close()

if __name__ == "__main__":
    apply_gdp()
