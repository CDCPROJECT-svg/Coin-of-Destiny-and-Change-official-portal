import sqlite3
import time
import os

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
YOUTUBE_LINK = "https://youtube.com/@codaccoinportalofficialchannel"

def clear():
    try: os.system('clear')
    except: pass

def check_duplicate(cur, identifier, id_type="email"):
    query = f"SELECT COUNT(*) FROM active_members WHERE {id_type} = ?"
    cur.execute(query, (identifier,))
    return cur.fetchone()[0] > 0

def auto_find_upline(cur):
    cur.execute("SELECT user_id, current_level FROM active_members ORDER BY current_level ASC, user_id ASC")
    all_members = cur.fetchall()
    for member in all_members:
        upline_id = member[0]
        cur.execute("SELECT COUNT(*) FROM active_members WHERE sponsor_id = ?", (upline_id,))
        if cur.fetchone()[0] < 2:
            return upline_id
    return "FOUNDER-001"

def universal_registration():
    clear()
    print("========================================================")
    print("   🌐 CODAC GLOBAL PORTAL | COMPREHENSIVE REGISTRATION")
    print("========================================================")
    
    # 1. YOUTUBE GATE
    if input(f"   📺 Subscribed to {YOUTUBE_LINK}? (YES/NO): ").strip().upper() != "YES":
        print("   ❌ Subscribe first.")
        return

    # 2. PRIVACY CONSENT
    print("\n   🛡️  DATA PRIVACY ACT COMPLIANCE: Accepted.")

    # 3. SELECT COUNTRY
    print("\n   🌍 COUNTRY SELECTION")
    country = input("   👉 Enter Country Code (e.g., PHIL): ").strip().upper()
    if len(country) < 2: country = "PHIL"

    # 4. SELECT CATEGORY
    print("\n   📂 SELECT CATEGORY:")
    print("   [1] INDIVIDUAL")
    print("   [2] MINOR (Newborn)")
    print("   [3] BUSINESS")
    print("   [4] ORGANIZATION")
    print("   [5] GOVERNMENT")
    
    choice = input("   👉 Enter Number: ").strip()
    
    account_type = "INDIVIDUAL"
    id_code = "IND"
    guardian_id = None
    doc_reg = None
    birth_cert = None
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # --- CATEGORY LOGIC ---
    if choice == "1":
        id_code = "IND"
    elif choice == "2": # MINOR
        account_type = "MINOR"
        id_code = "KID"
        print("\n   👶 MINOR REGISTRATION")
        guardian_id = input("   Enter Guardian ID: ").strip().upper()
        if not cur.execute("SELECT user_id FROM active_members WHERE user_id=?", (guardian_id,)).fetchone():
            print("   ❌ Guardian ID not found."); conn.close(); return
        birth_cert = input("   Enter Birth Cert No: ").strip()
    elif choice == "3": # BUSINESS
        account_type = "BUSINESS"
        id_code = "BIZ"
        print("\n   🏢 BUSINESS REGISTRATION")
        doc_reg = input("   Enter DTI/SEC Permit No: ").strip()
    elif choice == "4":
        account_type = "ORGANIZATION"
        id_code = "ORG"
        doc_reg = input("   Enter Org Reg No: ").strip()
    elif choice == "5":
        account_type = "GOVT_AGENCY"
        id_code = "GOV"
        print("\n   🏛️ GOVERNMENT AGENCY")
        doc_reg = input("   Enter Agency Charter/ID: ").strip()
    else:
        print("   ❌ Invalid."); conn.close(); return

    # 5. PERSONAL / ENTITY DETAILS
    name = input(f"   Enter Name ({account_type}): ").strip()
    
    print("\n   📍 CONTACT INFORMATION")
    address = input("   Complete Address: ").strip()
    contact = input("   Mobile/Tel Number: ").strip()

    # 6. DEMOGRAPHICS (Only for Humans)
    sex = "N/A"
    marital = "N/A"
    occupation = "N/A"

    if choice in ["1", "2"]: # INDIVIDUAL or MINOR
        print("\n   👤 DEMOGRAPHIC PROFILE")
        sex = input("   Sex (Male/Female): ").strip().upper()
        marital = input("   Marital Status (Single/Married/Widowed): ").strip().upper()
        occupation = input("   Occupation/Profession: ").strip().upper()
    else:
        # For Businesses, Occupation becomes Nature of Business
        occupation = input("\n   🏢 Nature of Business/Service: ").strip().upper()

    email = input("\n   Official Email: ").strip()
    if check_duplicate(cur, email):
        print("   🚫 Email Used."); conn.close(); return

    # 7. AUTO-PLACEMENT & ID GENERATION
    print("\n   ⚙️  Generating Global ID...")
    upline_id = auto_find_upline(cur)
    cur.execute("SELECT current_level, current_cycle FROM active_members WHERE user_id=?", (upline_id,))
    up_data = cur.fetchone()
    new_level = up_data[0] + 1
    cycle = up_data[1]
    
    cur.execute("SELECT COUNT(*) FROM active_members")
    count = cur.fetchone()[0] + 1
    
    new_id = f"{country}-{id_code}-C{cycle}-L{new_level}-{count:04d}"

    # 8. SAVE TO DATABASE
    try:
        query = """
            INSERT INTO active_members 
            (user_id, name, email, address, contact_number, sex, marital_status, occupation,
             country_code, sponsor_id, current_level, current_cycle, status, 
             account_type, guardian_id, dti_sec_reg, birth_certificate, 
             data_privacy_consent, is_kyc_verified, trading_points)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING_DOCS', ?, ?, ?, ?, 1, 0, 0)
        """
        cur.execute(query, (new_id, name, email, address, contact, sex, marital, occupation,
                            country, upline_id, new_level, cycle, 
                            account_type, guardian_id, doc_reg, birth_cert))
        conn.commit()
        
        print("\n   ✅ REGISTRATION SUCCESSFUL!")
        print("   ==========================================")
        print(f"   🆔 GLOBAL ID: {new_id}")
        print(f"   👤 Name:      {name}")
        if choice in ["1", "2"]:
            print(f"   ⚤ Sex/Status: {sex} / {marital}")
            print(f"   🔨 Job:       {occupation}")
        else:
            print(f"   🏢 Nature:    {occupation}")
        print(f"   📱 Contact:   {contact}")
        print("   ==========================================")
        print("   🔒 Status: PENDING VERIFICATION")
        
    except sqlite3.IntegrityError:
        print("   ❌ Error: Data Conflict.")
    
    conn.close()

if __name__ == "__main__":
    universal_registration()
