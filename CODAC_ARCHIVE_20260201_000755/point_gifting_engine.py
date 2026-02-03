import sqlite3
import sys

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"

def validate_relationship(cur, sender_id, receiver_id):
    """
    Checks if receiver is TRULY inside the sender's umbrella (Downline).
    Returns True if valid, False if Crossline/Upline.
    Uses Recursive Query to trace bloodline.
    """
    query = """
    WITH RECURSIVE umbrella AS (
        -- 1. Start with the Sender's direct recruits (Level 1 Downlines)
        SELECT user_id, sponsor_id FROM active_members WHERE sponsor_id = ?
        UNION ALL
        -- 2. Find the recruits of those recruits (Deep Levels)
        SELECT m.user_id, m.sponsor_id 
        FROM active_members m
        JOIN umbrella u ON m.sponsor_id = u.user_id
    )
    -- 3. Check if the Receiver exists in this generated list
    SELECT 1 FROM umbrella WHERE user_id = ?;
    """
    cur.execute(query, (sender_id, receiver_id))
    return cur.fetchone() is not None

def gift_points(sender_id, receiver_id, category, amount):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # --- CHECK 1: RECEIVER STATUS (Active/Inactive) ---
        cur.execute("SELECT status FROM active_members WHERE user_id = ?", (receiver_id,))
        row = cur.fetchone()
        
        if not row:
            print("❌ ERROR: Receiver ID not found.")
            return False
            
        receiver_status = row[0]
        if receiver_status in ['RED_FLAG', 'DEACTIVATED', 'INACTIVE']:
            print(f"⛔ BLOCKED: Receiver is {receiver_status}. Gifts cannot be sent to inactive accounts.")
            return False

        # --- CHECK 2: UMBRELLA VALIDATION (Downline Only) ---
        # If Sender is NOT the sponsor/ancestor of Receiver, block it.
        if not validate_relationship(cur, sender_id, receiver_id):
            print("⛔ BLOCKED: Violation of Vertical Flow Protocol.")
            print("   - You can only gift to your DOWNLINES (Under your Umbrella).")
            print("   - Crossline and Upline transfers are strictly PROHIBITED.")
            return False

        # --- CHECK 3: SENDER BALANCE ---
        cur.execute(f"SELECT {category} FROM active_members WHERE user_id = ?", (sender_id,))
        balance_row = cur.fetchone()
        
        if not balance_row or balance_row[0] < amount:
            print(f"❌ INSUFFICIENT FUNDS: You do not have enough {category}.")
            return False

        # --- EXECUTE TRANSFER ---
        cur.execute(f"UPDATE active_members SET {category} = {category} - ? WHERE user_id = ?", (amount, sender_id))
        cur.execute(f"UPDATE active_members SET {category} = {category} + ? WHERE user_id = ?", (amount, receiver_id))
        
        conn.commit()
        
        print(f"\n🎁 GIFT SUCCESSFUL!")
        print(f"✅ From Leader {sender_id} -> To Downline {receiver_id}")
        print(f"💎 Amount: {amount} {category}")
        return True

    except Exception as e:
        print(f"❌ SYSTEM ERROR: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    # Test Scenarios
    print("--- 🧪 TESTING SECURITY PROTOCOLS ---")
    
    # Example 1: Trying to gift to an Inactive/Red Flag account
    # (Assuming we manually set User 99 to RED_FLAG for testing)
    # gift_points('1', '99', 'trading_points', 100)

    # Example 2: Trying to gift to Upline (Leader) or Crossline
    # gift_points('5', '1', 'trading_points', 100) # Should FAIL
