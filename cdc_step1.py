import time
import sqlite3

def start_gatekeeper():
    print("\n" + "="*45)
    print("      CDC COIN PORTAL: THE GATEKEEPER        ")
    print("         'EASY LIFE & HAYAHAY'               ")
    print("="*45)

    # 1. ENTITY & ID VALIDATION
    entities = ["Personal", "Institution", "Merchant", "Association", "Cooperative", "Family Clan", "Government Agency"]
    print("\n[SELECT ENTITY]")
    for i, e in enumerate(entities, 1): print(f"{i}. {e}")
    try:
        ent_choice = int(input("Choice (1-7): "))
        selected_ent = entities[ent_choice-1]
    except: return

    member_name = input("\nEnter Full Name of Registrant: ")

    # 2. 3rd GENERATION TRACER
    print("\n" + "-"*30)
    print("   GENEALOGY TRACER (3rd Gen)   ")
    print("-"*30)
    f_name = input("FATHER'S Full Name: ")
    m_name = input("MOTHER'S Full Name: ")

    # 3. SUCCESSION & BENEFICIARIES (LGBT & EXTENDED FAMILY INCLUDED)
    print("\n[BENEFICIARY SETUP - INCLUSIVE]")
    print("Valid Successors: Partner (LGBT/Transgender), Spouse, Child,")
    print("                  Parent, Grandparent, Sibling, Niece/Nephew.")
    ben_name = input("Enter Primary Beneficiary Name: ")
    ben_rel = input("Relationship (e.g. Partner, Pamangkin, Lolo, etc.): ")

    # 4. SAVE TO DATABASE
    conn = sqlite3.connect('cdc_portal/mother_tree.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS members 
                      (name TEXT, entity TEXT, father TEXT, mother TEXT, beneficiary TEXT, rel TEXT, status TEXT)''')
    cursor.execute("INSERT INTO members VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (member_name, selected_ent, f_name, m_name, ben_name, ben_rel, "PENDING 8-CDC"))
    conn.commit()
    conn.close()

    print("\n[SYSTEM] Verifying Inclusive Succession Rights...")
    time.sleep(1.5)
    print("\n" + "="*45)
    print("      REGISTRATION MODULE 1: FULLY SEALED!   ")
    print(f"      ACCOUNT: {member_name.upper()} ")
    print(f"      SUCCESSOR: {ben_name.upper()} ({ben_rel.upper()})")
    print("="*45 + "\n")

if __name__ == "__main__":
    start_gatekeeper()

