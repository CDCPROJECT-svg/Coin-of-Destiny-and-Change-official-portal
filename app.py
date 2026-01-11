import os
import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS
from main_engine import CDCEngine

app = Flask(__name__)
CORS(app)
engine = CDCEngine()

# Secure Connection from Environment
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

def get_member_data(member_id):
    try:
        # Securely connecting to Supabase PostgreSQL
        conn = psycopg2.connect(SUPABASE_DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT project_id, leadership_title FROM members WHERE id=%s", (member_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row
    except Exception as e:
        print(f"Sovereign DB Error: {e}")
        return None

@app.route('/api/member/<int:member_id>')
def member_stats(member_id):
    data = get_member_data(member_id)
    if not data:
        return jsonify({"error": "Member not found in Global Registry"}), 404

    p_id, title = data
    # Protected CDCEngine Logic
    reward = engine.calculate_reward(cycle=1, project_id=p_id)
    
    return jsonify({
        "project_id": p_id,
        "leadership_title": title,
        "daily_withdrawal": round(reward * 0.08, 2),
        "total_worth": reward,
        "status": "SECURED_BY_SUPABASE"
    })

if __name__ == '__main__':
    # Checking if URL exists before starting
    if not SUPABASE_DB_URL:
        print("CRITICAL ERROR: SUPABASE_DB_URL not found in Environment Variables!")
    else:
        app.run(host='0.0.0.0', port=8080)
