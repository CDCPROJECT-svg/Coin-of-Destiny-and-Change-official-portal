import sqlite3
import webbrowser
import os

# PATHS
DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
OUTPUT_FILE = "/data/data/com.termux/files/home/codac-coin_portal/secure_session.html"

def connect_and_render():
    os.system('clear')
    print("--- 🔌 CODAC DATABASE RENDER ENGINE ---")
    
    # 1. AUTHENTICATION (Kunwari nag-login ka)
    user_id = "FOUNDER-001" 
    print(f"   👤 Authenticating User: {user_id}...")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 2. HUGUTIN ANG DATA MULA SA DB (Live Data)
    cur.execute("SELECT name, status, trading_points, merchant_points, channel_points, current_cycle FROM active_members WHERE user_id=?", (user_id,))
    user_data = cur.fetchone()

    if not user_data:
        print("   ❌ Error: User not found in DB.")
        return

    # 3. HUGUTIN ANG DESIGN MULA SA DB (Stored Interface)
    # Ito ang patunay na sa DB nakatago ang design, hindi sa labas.
    print("   🎨 Fetching Interface Template from 'system_interface' table...")
    cur.execute("SELECT html_content FROM system_interface WHERE view_name='homepage_master'")
    template_data = cur.fetchone()

    if not template_data:
        print("   ❌ Error: Interface Template not found in DB. Please run setup first.")
        return

    raw_html = template_data[0]

    # 4. PAGSAMAHIN ANG DATA AT DESIGN (Rendering)
    print("   ⚙️  Merging Live Database Data into View...")
    
    # Get Counts for dashboard
    cur.execute("SELECT COUNT(*) FROM active_members WHERE is_task_exempt=1")
    vip_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM active_members WHERE current_level > 9")
    organic_count = cur.fetchone()[0]
    target = 1048576

    conn.close()

    # Inject Data
    final_view = raw_html.format(
        founder_name=user_data[0],
        founder_id=user_id,
        status=user_data[1],
        trade_pts=f"{user_data[2]:,.2f}",
        merch_pts=f"{user_data[3]:,.2f}",
        chan_pts=f"{user_data[4]:,.2f}",
        cycle=user_data[5],
        vip_count=vip_count,
        organic_count=organic_count,
        target=f"{target:,}"
    )

    # 5. DISPLAY
    # Save temporarily just for the browser to see it, then it can be discarded.
    with open(OUTPUT_FILE, "w") as f:
        f.write(final_view)

    print(f"   ✅ SUCCESS: View Rendered from Database.")
    print(f"   👉 Opening Secure Session...")
    
    # Optional: Print preview in terminal
    print("\n   [PREVIEW OF DATA INJECTED]")
    print(f"   Name: {user_data[0]}")
    print(f"   Wallet: {user_data[2]:,.2f}")
    print(f"   Template Source: database/codac_master.db")

if __name__ == "__main__":
    connect_and_render()
