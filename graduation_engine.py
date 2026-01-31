import sqlite3

DB_PATH = "/data/data/com.termux/files/home/codac-coin_portal/database/codac_master.db"
TARGET_POINTS = 18888
REQUIRED_SLOTS = 1048576  # Perfect 20th Level Count

def check_perfect_20_readiness():
    print(f"\n--- 🏆 PERFECT 20TH LEVEL AUDIT (Capacity: {REQUIRED_SLOTS:,}) ---")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # 1. THE OVERTAKE QUERY
        # - Filter out RED FLAG status
        # - Must have >= 18,888 in ALL 3 categories
        # - ORDER BY Total Points DESC (This enables the "Overtake/Pass-up")
        query = """
            SELECT user_id, name, trading_points, merchant_points, channel_points,
                   (trading_points + merchant_points + channel_points) as total_score
            FROM active_members
            WHERE status != 'RED_FLAG'
            AND trading_points >= ?
            AND merchant_points >= ?
            AND channel_points >= ?
            ORDER BY total_score DESC
            LIMIT ?
        """
        
        cur.execute(query, (TARGET_POINTS, TARGET_POINTS, TARGET_POINTS, REQUIRED_SLOTS))
        qualified_members = cur.fetchall()
        
        count = len(qualified_members)
        
        print(f"📊 Qualified Candidates Found: {count:,}")
        
        if count == 0:
            print("❌ STATUS: No one has qualified yet.")
            return

        # 2. Display Top Performers (The new "Root" candidates)
        print("\n🚀 TOP PERFORMERS (Priority Placement):")
        print(f"{'ID':<5} {'NAME':<15} {'SCORE':<10} {'STATUS'}")
        print("-" * 40)
        
        for i, member in enumerate(qualified_members[:10]): # Show top 10 only
            user_id = member[0]
            name = member[1]
            score = member[5]
            print(f"{user_id:<5} {name:<15} {score:,.0f} {'✅ QUALIFIED'}")

        # 3. Graduation Check
        if count >= REQUIRED_SLOTS:
            print("\n🎉 SYSTEM ALERT: PERFECT 20TH LEVEL IS FULLY FORMED!")
            print("👉 The Root Leader can now Claim Grand Reward & Exit to Cycle 2.")
            print("👉 Triggering 'Point Distribution' Protocol...")
        else:
            needed = REQUIRED_SLOTS - count
            print(f"\n⏳ SYSTEM STATUS: BUILDING... Need {needed:,} more qualified members.")
            print("💡 Reminder: Inactive accounts are being skipped.")

    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_perfect_20_readiness()
