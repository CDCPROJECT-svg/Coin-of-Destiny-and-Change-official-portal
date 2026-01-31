from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==============================================================================
# 🎨 CENTRAL DESIGN SYSTEM (Dark & Gold Theme)
# ==============================================================================
BASE_CSS = """
<style>
    :root { --gold: #d4af37; --dark: #050505; --panel: #111; --text: #eee; --green: #00ff00; }
    body { background-color: var(--dark); color: var(--text); font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; padding-bottom: 60px; }
    
    /* HEADER */
    .header { background: #0a0a0a; border-bottom: 2px solid var(--gold); padding: 15px; text-align: center; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 10px rgba(212,175,55,0.1); }
    .logo { color: var(--gold); font-size: 24px; font-weight: bold; letter-spacing: 1px; margin: 0; }
    .sub-logo { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 2px; }

    /* CARDS */
    .card { background: var(--panel); border: 1px solid #333; border-radius: 12px; padding: 20px; margin: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
    .card-title { color: var(--gold); font-size: 14px; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 5px; text-transform: uppercase; }

    /* BUTTONS / MENU */
    .menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 0 15px; }
    .btn-menu { background: #151515; border: 1px solid #444; color: white; padding: 20px; text-align: center; border-radius: 10px; text-decoration: none; transition: 0.2s; display:block; }
    .btn-menu:hover { border-color: var(--gold); background: #222; transform: translateY(-2px); }
    .btn-icon { font-size: 28px; display: block; margin-bottom: 5px; }
    
    .btn-back { display: block; width: 120px; margin: 30px auto; text-align: center; color: #888; text-decoration: none; border: 1px solid #333; padding: 10px; border-radius: 20px; font-size: 12px; }

    /* BADGES */
    .badge { padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    .badge-green { background: rgba(0,255,0,0.1); color: var(--green); border: 1px solid var(--green); }
    
    /* VIRAL BOX */
    .viral-box { background: #0f150f; border: 1px dashed var(--gold); padding: 15px; font-family: 'Courier New', monospace; font-size: 13px; color: #ddd; white-space: pre-wrap; line-height: 1.4; }
</style>
"""

# ==============================================================================
# 1. HOMEPAGE (Dashboard)
# ==============================================================================
HOMEPAGE_HTML = """
<!DOCTYPE html>
<html>
<head><title>CODAC HQ</title><meta name="viewport" content="width=device-width, initial-scale=1">
""" + BASE_CSS + """
</head>
<body>
    <div class="header">
        <h1 class="logo">CODAC</h1>
        <div class="sub-logo">Central Banking Portal</div>
    </div>

    <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <h2 style="margin:0; font-size:18px;">{{ founder['user_id'] }}</h2>
                <div style="margin-top:5px;"><span class="badge badge-green">IMMUNE • CYCLE {{ founder['current_cycle'] }}</span></div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:10px; color:#888;">GRAND REWARD</div>
                <div style="font-size:20px; color:var(--gold); font-weight:bold;">${{ "{:,.2f}".format(founder['grand_reward_total']) }}</div>
            </div>
        </div>
    </div>

    <div class="menu-grid">
        <a href="/tree" class="btn-menu">
            <span class="btn-icon">🏛️</span>
            STRUCTURE
        </a>
        <a href="/viral" class="btn-menu">
            <span class="btn-icon">📢</span>
            VIRAL LINK
        </a>
        <a href="/wallet" class="btn-menu">
            <span class="btn-icon">💼</span>
            VAULT
        </a>
        <a href="/settings" class="btn-menu">
            <span class="btn-icon">⚙️</span>
            CONFIG
        </a>
    </div>

    <div class="card">
        <div class="card-title">🚀 SYSTEM LIVE STATUS</div>
        <p style="font-size:12px; color:#aaa; line-height:1.6;">
            ✅ Viral Engine: <b>DEPLOYED</b><br>
            ✅ Brand Message: <b>"HAYAHAY" ACTIVE</b><br>
            ✅ Hierarchy: <b>LEVEL 9 ANCHORED</b>
        </p>
    </div>
</body>
</html>
"""

# ==============================================================================
# 2. STRUCTURE PAGE (Tree View)
# ==============================================================================
TREE_HTML = """
<!DOCTYPE html>
<html>
<head><title>CODAC STRUCTURE</title><meta name="viewport" content="width=device-width, initial-scale=1">
""" + BASE_CSS + """
</head>
<body>
    <div class="header">
        <h1 class="logo">HIERARCHY</h1>
        <div class="sub-logo">Official Database View</div>
    </div>

    <div style="text-align:center; padding:20px;">
        <div style="display:inline-block; border:2px solid var(--gold); padding:15px; border-radius:10px; background:#111; margin-bottom:20px; box-shadow: 0 0 15px rgba(212,175,55,0.2);">
            👑 <b>{{ root['user_id'] }}</b><br>
            <span class="badge badge-green" style="margin-top:5px; display:inline-block;">ROOT NODE</span>
        </div>
        
        <div style="font-size:24px; color:#444;">⬇️</div>

        <div class="card">
            <h3 class="card-title">PIONEER LAYER (Levels 2-8)</h3>
            <p style="font-size:14px;">Verified VIPs: <b style="color:white">{{ vip_count }}</b></p>
        </div>

        <div style="font-size:24px; color:#444;">⬇️</div>

        <div class="card" style="border-color:var(--green);">
            <h3 class="card-title" style="color:var(--green);">🌍 LEVEL 9: COUNTRY FOUNDATION</h3>
            <div style="max-height:300px; overflow-y:auto; text-align:left; background:#000; padding:10px; border-radius:5px;">
                {% for c in countries %}
                <div style="border-bottom:1px solid #222; padding:8px 5px; font-size:12px; display:flex; justify-content:space-between;">
                    <span>🏳️ {{ c['user_id'] }}</span>
                    <span style="color:#444;">L9</span>
                </div>
                {% endfor %}
            </div>
            <p style="font-size:10px; text-align:center; margin-top:10px; color:#666;">Total Countries: {{ country_count }}</p>
        </div>
    </div>

    <a href="/" class="btn-back">← DASHBOARD</a>
</body>
</html>
"""

# ==============================================================================
# 3. VIRAL PAGE (The Message)
# ==============================================================================
VIRAL_HTML = """
<!DOCTYPE html>
<html>
<head><title>CODAC VIRAL</title><meta name="viewport" content="width=device-width, initial-scale=1">
""" + BASE_CSS + """
</head>
<body>
    <div class="header">
        <h1 class="logo">VIRAL ENGINE</h1>
        <div class="sub-logo">Public Expansion Tool</div>
    </div>

    <div class="card">
        <h3 class="card-title">📢 OFFICIAL BRAND MESSAGE</h3>
        <div class="viral-box">{{ viral_msg }}</div>
    </div>

    <div class="card">
        <h3 class="card-title">📺 OFFICIAL CHANNEL</h3>
        <p style="font-size:12px; color:#888;">Share this link to activate the "Watch-to-Earn" mindset:</p>
        <a href="{{ yt_link }}" target="_blank" style="color:var(--gold); word-break:break-all; font-weight:bold; font-size:14px;">{{ yt_link }}</a>
    </div>

    <div class="card">
        <h3 class="card-title">🔗 YOUR INVITE LINK</h3>
        <input type="text" value="https://codac-portal.com/join?ref=FOUNDER-001" style="width:90%; padding:15px; background:#000; border:1px solid #444; color:#fff; border-radius:5px; font-family:monospace;" readonly>
    </div>

    <a href="/" class="btn-back">← DASHBOARD</a>
</body>
</html>
"""

# ==============================================================================
# ROUTES (Backend Logic)
# ==============================================================================
@app.route('/')
def home():
    conn = get_db_connection()
    founder = conn.execute("SELECT * FROM active_members WHERE user_id='FOUNDER-001'").fetchone()
    conn.close()
    if not founder: return "<h3>Founder Not Found. Please Reset Database.</h3>"
    return render_template_string(HOMEPAGE_HTML, founder=founder)

@app.route('/tree')
def tree():
    conn = get_db_connection()
    root = conn.execute("SELECT * FROM active_members WHERE user_id='FOUNDER-001'").fetchone()
    vip_count = conn.execute("SELECT count(*) FROM active_members WHERE current_level BETWEEN 2 AND 8").fetchone()[0]
    countries = conn.execute("SELECT user_id FROM active_members WHERE current_level=9 ORDER BY user_id ASC").fetchall()
    conn.close()
    return render_template_string(TREE_HTML, root=root, vip_count=vip_count, countries=countries, country_count=len(countries))

@app.route('/viral')
def viral():
    conn = get_db_connection()
    # Fetch Message
    msg_row = conn.execute("SELECT value FROM system_config WHERE key='master_viral_msg'").fetchone()
    msg = msg_row['value'] if msg_row else "Message not deployed yet."
    
    # Fetch Link
    link_row = conn.execute("SELECT value FROM system_config WHERE key='official_youtube_link'").fetchone()
    link = link_row['value'] if link_row else "#"
    
    conn.close()
    return render_template_string(VIRAL_HTML, viral_msg=msg, yt_link=link)

@app.route('/wallet')
def wallet():
    return "<body style='background:#050505; color:#d4af37; font-family:sans-serif; text-align:center; padding:50px;'><h1>💼 CENTRAL VAULT</h1><p>Module Under Construction...</p><br><a href='/' style='color:#888; text-decoration:none; border:1px solid #444; padding:10px; border-radius:20px;'>← BACK</a></body>"

@app.route('/settings')
def settings():
    return "<body style='background:#050505; color:#d4af37; font-family:sans-serif; text-align:center; padding:50px;'><h1>⚙️ CONFIG</h1><p>Admin Controls Restricted</p><br><a href='/' style='color:#888; text-decoration:none; border:1px solid #444; padding:10px; border-radius:20px;'>← BACK</a></body>"

if __name__ == '__main__':
    print("------------------------------------------------")
    print(" 🚀 CODAC CENTRAL PORTAL IS LIVE")
    print(" 👉 ACCESS LINK: http://127.0.0.1:5000")
    print("------------------------------------------------")
    app.run(host='0.0.0.0', port=5000)
