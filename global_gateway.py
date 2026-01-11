import psycopg2
import requests

def get_db_connection():
    return psycopg2.connect(
        dbname='postgres',
        user='postgres.xzbozofttuvyijeimxkj',
        password='dnHmzMkSQhvMmCj8',
        host='aws-1-ap-south-1.pooler.supabase.com',
        port='6543',
        sslmode='require'
    )

def detect_geo_and_security(ip_address):
    # Detects country and checks for VPN/Proxy hackers
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/").json()
        return {
            "country": response.get("country_name", "Unknown"),
            "proxy": response.get("security", {}).get("is_proxy", False)
        }
    except:
        return {"country": "Unknown", "proxy": False}

def process_global_signup(user_email, full_name, father, mother, user_ip):
    conn = get_db_connection()
    cur = conn.cursor()
    
    geo_data = detect_geo_and_security(user_ip)
    
    # 1. ANCESTRAL CHECK
    cur.execute("SELECT id FROM the_forbidden_list WHERE full_name IN (%s, %s)", (father, mother))
    ancestor_match = cur.fetchone()
    
    if ancestor_match:
        # AUTO-COLLECT TO FORBIDDEN LIST
        cur.execute("INSERT INTO the_forbidden_list (full_name, reason) VALUES (%s, %s)", 
                    (full_name, f"Ancestral Link to ID: {ancestor_match[0]}"))
        status = 'ANCESTRAL_BLOCKED'
    elif geo_data['proxy']:
        # HACKER PROTECTION
        status = 'SUSPICIOUS_HIGH_RISK'
    else:
        status = 'PENDING_FOUNDER_REVIEW'

    # 2. CREATE GLOBAL CITIZEN RECORD
    cur.execute("""
        UPDATE citizens SET 
        father_name = %s, mother_name = %s, 
        country_name = %s, status = %s 
        WHERE email = %s
    """, (father, mother, geo_data['country'], status, user_email))
    
    conn.commit()
    cur.close()
    conn.close()
    return f"Status: {status} | Country: {geo_data['country']}"

if __name__ == "__main__":
    # Test simulation
    print("--- CDC GLOBAL GATEWAY TESTING ---")
    result = process_global_signup("test@example.com", "Juan Dela Cruz", "BlockedFather", "CleanMother", "1.1.1.1")
    print(result)
