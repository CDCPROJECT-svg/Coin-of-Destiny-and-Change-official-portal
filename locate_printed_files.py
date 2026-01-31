import os
import csv

# PATHS TO SEARCH
DOWNLOADS = "/data/data/com.termux/files/home/storage/downloads/"
REF_FOLDER = os.path.join(DOWNLOADS, "CODAC_OFFICIAL_REFERENCES")

def search_files():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🕵️  SEARCHING FOR YOUR PRINTED DOCUMENTS")
    print("=========================================================")

    # 1. SEARCH FOR BANKING STRUCTURE (Based on Image 2)
    print("\n[ 1. SEARCHING FOR: BANKING STRUCTURE ]")
    print("   (Target: MAIN-RESERVE, MAIN-TREASURY...)")
    
    bank_pdf = os.path.join(REF_FOLDER, "01_CENTRAL_BANKING_STRUCTURE.pdf")
    bank_txt = os.path.join(DOWNLOADS, "CODAC_BANKING_STRUCTURE_2026.txt")
    
    if os.path.exists(bank_pdf):
        print(f"   ✅ FOUND PDF: {bank_pdf}")
        print("      (This matches your 'CODAC CENTRALIZED BANKING' printout)")
    elif os.path.exists(bank_txt):
        print(f"   ✅ FOUND TXT: {bank_txt}")
    else:
        print("   ❌ Banking file not found in References.")

    # 2. SEARCH FOR COUNTRY LIST (Based on Image 1 & 3)
    print("\n[ 2. SEARCHING FOR: 204 COUNTRIES LIST ]")
    print("   (Target: Afghanistan, Albania, Algeria...)")
    
    # Check the Deployment CSV we just made
    csv_file = os.path.join(DOWNLOADS, "CODAC_OFFICIAL_204_DEPLOYMENT.csv")
    pdf_vault = os.path.join(REF_FOLDER, "03_MASTER_PRIVATE_KEYS_SECURE.pdf")
    
    if os.path.exists(csv_file):
        print(f"   ✅ FOUND CSV: {csv_file}")
        print("      (Contains Name, Wallet, and Private Key for Deployment)")
        
        # Verify Content Matches Image 3
        try:
            with open(csv_file, "r") as f:
                reader = csv.reader(f)
                next(reader) # Skip header
                first_row = next(reader)
                print(f"      🔎 CONTENT CHECK: First Entry is '{first_row[1]}'")
                if "Afghan" in first_row[1]:
                    print("      ✅ MATCHES YOUR PHOTO (Afghanistan is first)!")
        except:
            pass

    if os.path.exists(pdf_vault):
        print(f"   ✅ FOUND PDF VAULT: {pdf_vault}")
        print("      (This is the printable version with keys)")

    print("-" * 57)
    print("SUMMARY:")
    print("1. BANKING DOC  ---> Downloads/CODAC_OFFICIAL_REFERENCES/01_CENTRAL_BANKING_STRUCTURE.pdf")
    print("2. COUNTRY LIST ---> Downloads/CODAC_OFFICIAL_204_DEPLOYMENT.csv")
    print("=========================================================")

if __name__ == "__main__":
    search_files()
