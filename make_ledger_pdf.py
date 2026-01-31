import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
PDF_FILE = "/data/data/com.termux/files/home/codac-coin_portal/CODAC_MASTER_LEDGER.pdf"

def create_pdf():
    if not os.path.exists(DB_PATH):
        print("❌ Database not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    c = canvas.Canvas(PDF_FILE, pagesize=letter)
    width, height = letter
    y = height - 50

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "CODAC MASTER LEDGER - OFFICIAL PIONEER RECORDS")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30

    # Table Headers
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "PORTAL ID")
    c.drawString(220, y, "ACCOUNT NAME")
    c.drawString(410, y, "BALANCE (CODAC)")
    c.drawString(510, y, "LOCKED")
    y -= 10
    c.line(50, y, 560, y)
    y -= 15

    # Fetch Data
    cur.execute("SELECT user_id, name, trading_points, locked_balance FROM active_members ORDER BY is_system_account DESC, user_id ASC")
    rows = cur.fetchall()

    c.setFont("Helvetica", 8)
    for row in rows:
        uid, name, balance, locked = row
        
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y, "PORTAL ID (Continued...)")
            y -= 20

        c.drawString(50, y, str(uid))
        c.drawString(220, y, str(name)[:35])
        c.drawString(410, y, f"{balance:,.4f}")
        c.drawString(510, y, f"{locked:,.2f}")
        y -= 12

    c.save()
    conn.close()
    print(f"\n✅ PDF SUCCESS: Official Ledger saved as {PDF_FILE}")

if __name__ == "__main__":
    create_pdf()
