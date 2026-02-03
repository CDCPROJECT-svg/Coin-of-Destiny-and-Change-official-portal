from fpdf import FPDF
import sqlite3
import os

# CONFIGURATION
DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
DOWNLOADS_DIR = "/data/data/com.termux/files/home/storage/downloads/"
MARGIN = 12.7  # 0.5 inches in mm

# THE 7 CENTRAL BANKING PILLARS (ID, Display Name, Function Description)
BANKING_STRUCTURE = [
    ("MAIN-RESERVE", "FOUNDER PORTAL RESERVE", "Source: 128 Reserve Nodes (L08-001 to 128)"),
    ("MAIN-TREASURY", "FOUNDER PORTAL TREASURY", "Source: 64 Treasury Nodes (064 to 127)"),
    ("MAIN-GLOBAL", "GLOBAL PORTAL REWARD", "Source: 42 Global Specs (SPEC-011 to 052)"),
    ("MAIN-SUCCESSION", "SUCCESSION RESERVE", "Source: 7 Founder Accts (FOUNDER-001 to 007)"),
    ("MAIN-COFOUNDER", "CO-FOUNDER RESERVE", "Source: 8 Co-Founder Accts (008 to 015)"),
    ("MAIN-MANAGEMENT", "CODAC MAIN MANAGEMENT", "Source: 32 Dept Nodes (DEPT-032 to 063)"),
    ("MAIN-TEAM", "PORTAL TEAM ACCOUNT", "Source: 16 Team Nodes (TEAM-016 to 031)")
]

class BankingPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_margins(MARGIN, MARGIN, MARGIN)
        self.set_auto_page_break(auto=True, margin=MARGIN)

    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 8, "CODAC CENTRAL BANKING AUTHORITY", 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 6, "OFFICIAL MASTER KEY REGISTRY", 0, 1, 'C')
        self.line(MARGIN, 25, 210-MARGIN, 25)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'STRICTLY CONFIDENTIAL - FOUNDER EYES ONLY', 0, 0, 'C')

def create_vault():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    pdf = BankingPDF()
    pdf.add_page()
    
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🏦 GENERATING BANKING VAULT PDF...")
    print("=========================================================")

    for uid, name, func in BANKING_STRUCTURE:
        # Fetch Key
        cur.execute("SELECT wallet_address, private_key FROM active_members WHERE user_id = ?", (uid,))
        row = cur.fetchone()
        
        # If specific ID not found, try to find by Name or put Placeholder
        if row:
            wallet, pkey = row
        else:
            # Fallback check (Just in case IDs differ)
            wallet = "ADDRESS_NOT_FOUND_IN_DB"
            pkey = "KEY_NOT_FOUND_IN_DB"
            
        clean_key = pkey if pkey else "MISSING"
        clean_wallet = wallet if wallet else "MISSING"

        # --- PDF LAYOUT PER ACCOUNT ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 6, f"{name.upper()}", 0, 1) # ACCOUNT NAME
        
        pdf.set_font("Arial", 'I', 10)
        pdf.set_text_color(100, 100, 100) # Gray color for function
        pdf.cell(0, 6, f"Function: {func}", 0, 1) # FUNCTION
        pdf.set_text_color(0, 0, 0) # Reset color

        pdf.ln(2)
        
        pdf.set_font("Courier", '', 9) # Monospace for codes
        pdf.cell(25, 5, "WALLET:", 0, 0)
        pdf.cell(0, 5, clean_wallet, 0, 1)
        
        pdf.cell(25, 5, "PRIV KEY:", 0, 0)
        pdf.multi_cell(0, 5, clean_key, 0, 1)
        
        pdf.ln(5)
        pdf.line(MARGIN, pdf.get_y(), 210-MARGIN, pdf.get_y()) # Separator Line
        pdf.ln(5)
        
        print(f"   ✅ Processed: {name}")

    filename = os.path.join(DOWNLOADS_DIR, "CODAC_CENTRAL_BANK_VAULT.pdf")
    pdf.output(filename)
    
    print("-" * 57)
    print(f"   📄 PDF SAVED: {filename}")
    print("   Ready for printing.")
    
    conn.close()

if __name__ == "__main__":
    create_vault()
