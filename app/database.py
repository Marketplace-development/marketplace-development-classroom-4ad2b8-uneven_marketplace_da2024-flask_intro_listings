import psycopg2
import os

def get_db_connection():
    """Establish a connection to the database."""
    DATABASE_URL = os.getenv("postgresql://postgres.rfgfcpljgfwblooetbms:[CulinaryHeritage123è]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres")  # Fetch the database connection string from environment variables
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set.")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise