import sqlite3
import os

def update_viral_message():
    db_path = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # THE OFFICIAL ENGLISH MESSAGE
    new_msg = """Do you think that spending leads to depletion, and leisure leads to lack? In CODAC, every expense and moment of leisure contributes to the progress of all. To GOD be All the GLORY! Welcome to CODAC-Coin, a COIN of DESTINY & CHANGE where life becomes Easy and STRESS-FREE. This is not just a cryptocurrency; it is a Movement for true freedom. Together, let us build a system where watching, spending, and being a consumer are no longer causes of poverty—instead, they will bring comfort to all.

📢 SPREAD THE MESSAGE: Please share our YouTube Channel with your family, friends, and colleagues. Let us unite to change the world, one viewer at a time.

While you watch, you strengthen our network. The old "luxury" is now "help" for the transformation of your life and the world."""

    try:
        # Update the configuration key
        cursor.execute("UPDATE system_config SET value = ? WHERE key='master_viral_msg'", (new_msg,))
        conn.commit()
        print("------------------------------------------------")
        print(" ✅ VIRAL MESSAGE UPDATED TO ENGLISH")
        print(" 📄 Content: '...COIN of DESTINY & CHANGE...'")
        print("------------------------------------------------")
    except Exception as e:
        print(f" ❌ ERROR: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_viral_message()
