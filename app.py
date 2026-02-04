from flask import Flask, render_template_string, send_from_directory, request
import sqlite3
import os

app = Flask(__name__)
BASE_DIR = os.path.expanduser("~/codac-coin_portal")
DB_PATH = os.path.join(BASE_DIR, "database/codac_master.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 1. RESTORE ACCESS TO YOUR BUSINESS TEST FILE
@app.route('/business_test.html')
def business_test():
    return send_from_directory(BASE_DIR, 'business_test.html')

# 2. THE MASTER DASHBOARD (Linking your UI and Data)
@app.route('/')
def home():
    conn = get_db()
    # Pulling your specific stats (103 Points, etc.)
    user = conn.execute("SELECT * FROM active_members WHERE user_id='FOUNDER-001'").fetchone()
    
    # Accurate Count for Binary Monitor
    pioneers = conn.execute("SELECT COUNT(*) FROM active_members WHERE current_level >= 2 AND current_level <= 8").fetchone()[0]
    countries = conn.execute("SELECT COUNT(*) FROM active_members WHERE current_level = 9").fetchone()[0]
    max_lvl = conn.execute("SELECT MAX(current_level) FROM active_members").fetchone()[0]
    conn.close()

    return render_template_string(MAIN_UI, user=user, p_count=pioneers, c_count=countries, depth=max_lvl)

# THE UI YOU PROVIDED (Integrated with logic)
MAIN_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>CODAC | MASTER HUB</title>
    <style>
        body { background: #050505; color: #eee; font-family: sans-serif; margin: 0; padding: 15px; }
        .gold { color: #d4af37; }
        .card { border: 1px solid #333; padding: 15px; border-radius: 10px; margin-bottom: 10px; background: #111; }
        .grid-levels { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; }
        .lvl { padding: 5px; border: 1px solid #444; text-align: center; font-size: 10px; border-radius: 4px; }
        .active { border-color: #00ff00; color: #00ff00; }
        a { color: #d4af37; text-decoration: none; }
    </style>
</head>
<body>
    <h2 class="gold">CODAC COIN OF DESTINY & CHANGE</h2>
    <p>Empowering Communities • Creating Wealth</p>
    
    <div class="card">
        <p>💎 Reserve: <span class="gold">Active</span> | 🏦 Treasury: <span class="gold">Active</span></p>
        <p>Founder: <b>Uday</b> | Succession: <span style="color:#00ff00">Verified</span></p>
        <hr>
        <p>CODAC Points: <b>{{ user.trading_points }}</b></p>
        <p>Total CODAC Earned: <b>{{ user.grand_reward_total }}</b></p>
    </div>

    <div class="card">
        <h3 class="gold">💼 CODAC MASTER HUB</h3>
        <a href="/business_test.html">🚀 OPEN BUSINESS ENGINE</a><br><br>
        <a href="/tree">🌳 VIEW GENEALOGY ({{ p_count }} Pioneers / {{ c_count }} Countries)</a>
    </div>

    <div class="card">
        <p class="gold">🌳 BINARY MONITOR (L28)</p>
        <div class="grid-levels">
            {% for i in range(1, 29) %}
            <div class="lvl {% if i <= depth %}active{% endif %}">L{{ i }}</div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/tree')
def tree():
    conn = get_db()
    members = conn.execute("SELECT user_id, current_level FROM active_members ORDER BY current_level ASC").fetchall()
    conn.close()
    output = "<h1>NETWORK STRUCTURE</h1><ul>"
    for m in members:
        output += f"<li>{m['user_id']} (Level {m['current_level']})</li>"
    output += "</ul><br><a href='/'>Back</a>"
    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
