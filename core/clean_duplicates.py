import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

# LIST OF OLD NAMES TO REMOVE (To keep the new, formal ones)
DUPLICATES_TO_REMOVE = [
    "Bosnia",               # Keeping "Bosnia and Herzegovina"
    "Cape Verde",           # Keeping "Cabo Verde"
    "Congo (DRC)",          # Keeping "Democratic Republic of the Congo"
    "Congo (Rep)",          # Keeping "Congo"
    "Timor-Leste",          # Keeping "East Timor"
    "Saint Kitts",          # Keeping "Saint Kitts and Nevis"
    "Sao Tome",             # Keeping "Sao Tome and Principe"
    "Ivory Coast",          # Check if "Cote d'Ivoire" exists? (Optional)
    "Czech Republic"        # Check if "Czechia" exists? (Optional)
]

def clean_up():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- CODAC DATABASE CLEANER ---")
    print(f"Current Total: {cursor.execute("SELECT count(*) FROM active_members WHERE user_id LIKE 'CODAC-A09L%'").fetchone()[0]}")
    
    deleted_count = 0
    
    for name in DUPLICATES_TO_REMOVE:
        # Check if the duplicate exists
        cursor.execute("SELECT user_id FROM active_members WHERE name = ?", (name,))
        row = cursor.fetchone()
        
        if row:
            uid = row[0]
            print(f"Removing Duplicate: {name} (ID: {uid})")
            
            # Delete from members and vault
            cursor.execute("DELETE FROM active_members WHERE user_id = ?", (uid,))
            cursor.execute("DELETE FROM secure_vault WHERE user_id = ?", (uid,))
            deleted_count += 1
        else:
            pass # Name not found, safe.

    conn.commit()
    
    # FINAL CHECK
    cursor.execute("SELECT count(*) FROM active_members WHERE user_id LIKE 'CODAC-A09L%'")
    new_total = cursor.fetchone()[0]
    
    print("\n" + "="*40)
    print(f"Deleted: {deleted_count} Duplicates")
    print(f"NEW TOTAL: {new_total}")
    print("="*40)
    
    if new_total > 204:
        diff = new_total - 204
        print(f"⚠️ Still {diff} over the limit. We need to find the last ones manually.")
        # List all to see
        print("\nDisplaying full list to spot remaining duplicates:")
        cursor.execute("SELECT name FROM active_members WHERE user_id LIKE 'CODAC-A09L%' ORDER BY name ASC")
        for r in cursor.fetchall():
            print(f"- {r[0]}")
            
    conn.close()

if __name__ == "__main__":
    clean_up()
