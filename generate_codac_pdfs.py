from fpdf import FPDF
import sqlite3
import os

# CONFIGURATION
DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
DOWNLOADS_DIR = "/data/data/com.termux/files/home/storage/downloads/"

# 0.5 inches is approximately 12.7 mm
MARGIN = 12.7 

class PDF(FPDF):
    def __init__(self, title_text):
        super().__init__('P', 'mm', 'A4')
        self.title_text = title_text
        self.set_margins(MARGIN, MARGIN, MARGIN)
        self.set_auto_page_break(auto=True, margin=MARGIN)

    def header(self):
        # Logo / Header Text
        self.set_font('Arial', 'B', 14)
        self.cell(0, 8, "CODAC COIN PROJECT", 0, 1, 'C')
        self.set_font('Arial', 'B', 10)
        self.cell(0, 6, self.title_text, 0, 1, 'C')
        self.line(MARGIN, 25, 210-MARGIN, 25) # Line below header
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdfs():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\033[H\033[J", end="") # Clear Screen
    print("=========================================================")
    print("      📄 CODAC PDF DOCUMENT GENERATOR")
    print("=========================================================")

    # 1. GENERATE PRIVATE KEYS PDF
    print("   1️⃣  Creating PRIVATE KEY VAULT (A4)...")
    pdf_priv = PDF("MASTER VAULT - PRIVATE KEYS (STRICTLY CONFIDENTIAL)")
    pdf_priv.add_page()
    pdf_priv.set_font("Courier", size=9) # Monospace for keys

    cur.execute("SELECT user_id, name, private_key FROM active_members ORDER BY user_id")
    for row in cur.fetchall():
        uid, name, pkey = row
        clean_key = pkey if pkey else "MISSING"
        
        # Format: ID | Name
        pdf_priv.set_font("Arial", 'B', 9)
        pdf_priv.cell(0, 5, f"{uid} : {name}", 0, 1)
        
        # Format: Private Key
        pdf_priv.set_font("Courier", '', 9)
        pdf_priv.multi_cell(0, 5, f"KEY: {clean_key}", 0, 1)
        pdf_priv.ln(2) # Spacing

    file_priv = os.path.join(DOWNLOADS_DIR, "CODAC_PRIVATE_VAULT.pdf")
    pdf_priv.output(file_priv)
    print(f"      ✅ Saved: {file_priv}")

    # 2. GENERATE PUBLIC ADDRESS PDF
    print("\n   2️⃣  Creating PUBLIC DIRECTORY (A4)...")
    pdf_pub = PDF("PUBLIC DIRECTORY - WALLET ADDRESSES")
    pdf_pub.add_page()
    
    cur.execute("SELECT user_id, name, wallet_address FROM active_members ORDER BY user_id")
    for row in cur.fetchall():
        uid, name, wallet = row
        clean_wallet = wallet if wallet else "MISSING"
        
        # Format: ID | Name
        pdf_pub.set_font("Arial", 'B', 9)
        pdf_pub.cell(0, 5, f"{uid} : {name}", 0, 1)
        
        # Format: Wallet Address
        pdf_pub.set_font("Courier", '', 9)
        pdf_pub.cell(0, 5, f"ADDR: {clean_wallet}", 0, 1)
        pdf_pub.ln(2) # Spacing

    file_pub = os.path.join(DOWNLOADS_DIR, "CODAC_PUBLIC_DIRECTORY.pdf")
    pdf_pub.output(file_pub)
    print(f"      ✅ Saved: {file_pub}")

    print("-" * 57)
    print("   ✅ SUCCESS! Both PDFs are in your Downloads folder.")
    conn.close()

if __name__ == "__main__":
    generate_pdfs()
