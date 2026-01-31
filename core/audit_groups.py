import sqlite3
import os

DB_PATH = os.path.expanduser("~/codac-coin_portal/database/codac_master.db")

def audit_groups():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all sorted by Tier (1 first) then by ID
    cursor.execute("""
        SELECT user_id, name, gdp_tier 
        FROM active_members 
        WHERE user_id LIKE 'CODAC-A09L%' 
        ORDER BY gdp_tier ASC, user_id ASC
    """)
    all_countries = cursor.fetchall()

    group_a = all_countries[:118]
    group_b = all_countries[118:]

    print("\n" + "="*60)
    print("      CODAC COIN PORTAL - FINAL DISTRIBUTION AUDIT")
    print("="*60)

    print(f"\n[GROUP A: POOREST/PRIORITY] - Count: {len(group_a)}")
    print(f"Reward: 1,888,888 CODAC each")
    print("-" * 30)
    # Print first 5 and last 5 for brevity
    for c in group_a[:5]: print(f" - {c[1]}")
    print("   ...")
    for c in group_a[-5:]: print(f" - {c[1]}")

    print(f"\n[GROUP B: DEVELOPED/OTHERS] - Count: {len(group_b)}")
    print(f"Reward: 888,888 CODAC each")
    print("-" * 30)
    for c in group_b[:5]: print(f" - {c[1]}")
    print("   ...")
    for c in group_b[-5:]: print(f" - {c[1]}")

    print("\n" + "="*60)
    total_needed = (len(group_a) * 1888888) + (len(group_b) * 888888)
    print(f"TOTAL COINS REQUIRED FOR FEE DISTRO: {total_needed:,.0f}")
    print(f"SYSTEM TOTAL: {len(all_countries)} / 204")
    print("="*60)

    conn.close()

if __name__ == "__main__":
    audit_groups()
