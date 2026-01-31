import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname='postgres',
        user='postgres.xzbozofttuvyijeimxkj',
        password='dnHmzMkSQhvMmCj8',
        host='aws-1-ap-south-1.pooler.supabase.com',
        port='6543',
        sslmode='require'
    )

def toggle_ai_mode(on=True):
    # This updates a global setting for the portal
    mode = "AI AUTO-APPROVE" if on else "MANUAL FOUNDER REVIEW"
    print(f"⚙️ SYSTEM UPDATE: Portal is now in {mode} mode.")

def view_tracked_bloodlines():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT full_name, reason, blocked_date FROM the_forbidden_list ORDER BY blocked_date DESC")
    rows = cur.fetchall()
    print("\n--- 🩸 ANCESTRAL BLACKLIST: CURRENT TRACE ---")
    for row in rows:
        print(f"NAME: {row[0]} | REASON: {row[1]} | DATE: {row[2]}")
    cur.close()
    conn.close()

if __name__ == "__main__":
    print("1. Toggle AI Mode\n2. View Forbidden Bloodlines\n3. Manual Approve User")
    choice = input("Select Action: ")
    if choice == "2":
        view_tracked_bloodlines()
