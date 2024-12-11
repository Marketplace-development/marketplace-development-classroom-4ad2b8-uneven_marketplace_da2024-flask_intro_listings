import psycopg2

try:
    conn = psycopg2.connect("postgresql://postgres:CulinaryHeritage123ç@aws-0-eu-central-1.pooler.supabase.com:6543/postgres")
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")