import sqlite3
import os
from fpdf import FPDF
import datetime

# CONFIGURATION
DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
# DIRECT PATH TO DOWNLOADS (Para makita mo agad)
OUT_DIR = "/sdcard/Download/"
TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

class VaultPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, "CODAC COIN - MASTER VAULT", 0, 1, 'C')
        self.set_font('Arial', 'I', 8)
        self.cell(0, 5, f"OFFICIAL FINAL VERSION | Generated: {TIMESTAMP}", 0, 1, 'C')
        self.line(10, 25, 200, 25)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | CONFIDENTIAL OWNER: FOUNDER-001', 0, 0, 'C')

def generate_vault():
    print("\033[H\033[J", end="")
    print("=========================================================")
    print("      🔐 GENERATING MASTER VAULT (FINAL COMPLETE)")
    print("=========================================================")

    if not os.path.exists(DB_PATH):
        print("❌ ERROR: Database not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # FILES
    file_txt = os.path.join(OUT_DIR, "CODAC_MASTER_VAULT_FINAL.txt")
    file_pdf = os.path.join(OUT_DIR, "CODAC_MASTER_VAULT_FINAL.pdf")

    # 1. SETUP PDF
    pdf = VaultPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Courier", size=8) # Monospace for keys

    # 2. QUERY ALL DATA
    # Order: System Accounts first, then Countries, then others
    query = """
        SELECT user_id, name, wallet_address, private_key, is_system_account 
        FROM active_members 
        ORDER BY is_system_account DESC, user_id ASC
    """
    cur.execute(query)
    rows = cur.fetchall()
    
    total_count = len(rows)
    print(f"   📊 Processing {total_count} Total Accounts...")

    # 3. WRITE BOTH FILES SIMULTANEOUSLY
    with open(file_txt, "w") as f_txt:
        # TXT Header
        f_txt.write("================================================================\n")
        f_txt.write("   CODAC COIN - MASTER VAULT (FINAL COMPLETE VERSION)\n")
        f_txt.write(f"   Date: {TIMESTAMP}\n")
        f_txt.write("   WARNING: STRICTLY CONFIDENTIAL. DO NOT SHARE.\n")
        f_txt.write("================================================================\n\n")

        for row in rows:
            uid, name, wallet, pkey = row[0], row[1], row[2], row[3]
            
            # Label Section based on Account Type
            is_sys = row[4]
            section = "MEMBER"
            if is_sys == 99: section = "SYSTEM/BANKING"
            elif uid.startswith("PROJ"): section = "PROJECT"
            elif uid.startswith("CYCLE"): section = "PROJECT CYCLE"
            
            # --- WRITE TO TXT ---
            f_txt.write(f"[{section}] {uid}\n")
            f_txt.write(f"NAME:   {name}\n")
            f_txt.write(f"ADDR:   {wallet}\n")
            f_txt.write(f"KEY:    {pkey}\n")
            f_txt.write("-" * 60 + "\n")

            # --- WRITE TO PDF ---
            # Title (Bold)
            pdf.set_font("Arial", 'B', 9)
            pdf.set_fill_color(230, 230, 230) # Light Gray background for Name
            pdf.cell(0, 6, f"[{section}] {uid} : {name}", 0, 1, 'L', fill=True)
            
            # Data (Courier)
            pdf.set_font("Courier", '', 8)
            pdf.cell(20, 4, "ADDRESS:", 0, 0)
            pdf.cell(0, 4, wallet, 0, 1)
            pdf.cell(20, 4, "PRIV KEY:", 0, 0)
            pdf.multi_cell(0, 4, pkey, 0, 1)
            pdf.ln(2)

    # FINISH
    pdf.output(file_pdf)
    conn.close()

    print("-" * 57)
    print("   ✅ SUCCESS! Master Vault Generated.")
    print(f"   📄 Text File: CODAC_MASTER_VAULT_FINAL.txt")
    print(f"   📄 PDF File:  CODAC_MASTER_VAULT_FINAL.pdf")
    print("   📍 Location:  Downloads Folder (Check now!)")
    print("=========================================================")

if __name__ == "__main__":
    generate_vault()
