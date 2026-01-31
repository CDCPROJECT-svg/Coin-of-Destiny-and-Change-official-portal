import sqlite3
import csv
import os

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
EXPORT_FILE = "/sdcard/Download/CODAC_ALL_COUNTRIES_FORMATTED.csv"

def process_all():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🌍 FORMATTING & EXTRACTING ALL COUNTRIES (A-Z)")
    print("      Format: CODAC-A09L-Xxx-000-000-000")
    print("=========================================================")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. FETCH ALL TARGETS (No Limit)
    # Exclude System (99) and Projects/Teams
    cur.execute("""
        SELECT rowid, name 
        FROM active_members 
        WHERE is_system_account != 99 
        AND user_id NOT LIKE 'PROJ%' 
        AND user_id NOT LIKE 'CYCLE%'
        AND user_id NOT LIKE 'TEAM%'
        AND user_id NOT LIKE 'DEPT%'
        AND user_id != 'FOUNDER-001'
        ORDER BY name ASC
    """)
    rows = cur.fetchall()

    total = len(rows)
    print(f"   📊 Processing {total} Countries/Members...")
    print("   🔄 Updating IDs to official format...")

    # 2. UPDATE IDs
    count = 1
    for row in rows:
        rowid, name = row
        
        # Get 3-Letter Code (e.g., Sudan -> Sud)
        clean_name = name.replace(" ", "")
        code = clean_name[:3].capitalize()
        
        # Generate Sequence (e.g., 001, 195)
        seq = f"{count:03d}"
        
        # New ID Format
        new_id = f"CODAC-A09L-{code}-000-000-{seq}"
        
        cur.execute("UPDATE active_members SET user_id = ? WHERE rowid = ?", (new_id, rowid))
        count += 1

    conn.commit()
    print("   ✅ IDs Updated successfully.")

    # 3. EXTRACT TO CSV
    print("   🚀 Exporting to CSV...")
    
    cur.execute("""
        SELECT user_id, name, wallet_address, private_key 
        FROM active_members 
        WHERE user_id LIKE 'CODAC-A09L%'
        ORDER BY name ASC
    """)
    final_rows = cur.fetchall()

    with open(EXPORT_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "COUNTRY_NAME", "WALLET_ADDRESS", "PRIVATE_KEY"])
        writer.writerows(final_rows)

    print("-" * 57)
    print(f"   ✅ EXPORT COMPLETE: {len(final_rows)} Entries Saved.")
    print(f"   📂 File: CODAC_ALL_COUNTRIES_FORMATTED.csv")
    print(f"   📍 Location: Downloads Folder")

    # 4. VERIFICATION
    print("\n   🔎 CHECKING KEY COUNTRIES:")
    # Check France
    france = next((r for r in final_rows if "France" in r[1]), None)
    if france: print(f"      🇫🇷 {france[0]} | {france[1]}")
    
    # Check Philippines
    ph = next((r for r in final_rows if "Philippines" in r[1]), None)
    if ph: print(f"      🇵🇭 {ph[0]} | {ph[1]}")
    
    # Check Sudan
    sudan = next((r for r in final_rows if "Sudan" in r[1]), None)
    if sudan: print(f"      🇸🇩 {sudan[0]} | {sudan[1]}")

    conn.close()
    print("=========================================================")

if __name__ == "__main__":
    process_all()
