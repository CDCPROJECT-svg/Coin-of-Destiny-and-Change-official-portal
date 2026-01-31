import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def check_logic():
    print("--- CODAC BINARY LOGIC AUDIT ---")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Check if Extension Tracker is ready for infinite feeding
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='extension_tracker'")
    if cursor.fetchone():
        print("✅ extension_tracker Table: FOUND")
    else:
        print("❌ extension_tracker Table: MISSING")

    # 2. Check depth settings in config
    cursor.execute("SELECT key, value FROM system_config WHERE key LIKE '%DEPTH%'")
    configs = cursor.fetchall()
    print("\n--- Current Depth Limits ---")
    if configs:
        for k, v in configs:
            print(f"{k}: {v}")
    else:
        print("⚠️ No depth limits found in system_config.")

    conn.close()

if __name__ == "__main__":
    check_logic()
