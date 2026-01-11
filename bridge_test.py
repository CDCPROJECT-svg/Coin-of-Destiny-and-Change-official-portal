import psycopg2
import os

clusters = [
    "aws-0-ap-southeast-1.pooler.supabase.com",
    "aws-1-ap-southeast-1.pooler.supabase.com",
    "aws-0-ap-south-1.pooler.supabase.com",
    "aws-1-ap-south-1.pooler.supabase.com"
]

password = "YOUR_ACTUAL_PASSWORD"
user = "postgres.xzbozofttuvyijeimxkj"

for host in clusters:
    print(f"🔍 Testing {host}...")
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port='6543',
            sslmode='require',
            connect_timeout=5
        )
        print(f"✅ SUCCESS! Connected to {host}")
        conn.close()
        break
    except Exception as e:
        if "authentication failed" in str(e):
            print(f"🔑 SERVER FOUND at {host}, but password was wrong.")
            break
        else:
            print(f"❌ Not at {host}")
