from database import get_db_connection
import os

# Debug: Print DATABASE_URL
print("DATABASE_URL:", os.getenv("postgresql://postgres.rfgfcpljgfwblooetbms:CulinaryHeritage123è@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"))

try:
    conn = get_db_connection()
    print("Database connection successful!")
    conn.close()
except Exception as e:
    print(f"Failed to connect to the database: {e}")


