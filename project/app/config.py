from supabase import create_client, Client


class Config:
    SECRET_KEY = "a_really_long_and_random_string_1234567890!@#$%^&*()"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.pukfiejqjaztcjjekaty:Groep21dataalgo@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SUPABASE_URL = 'https://pukfiejqjaztcjjekaty.supabase.co'  # Vervang door je Supabase URL
    SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1a2ZpZWpxamF6dGNqamVrYXR5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyOTY4NzY3NywiZXhwIjoyMDQ1MjYzNjc3fQ.8LiTPrxfE3NCDNQqhEOfrjWj6kSGQxu6Z2B1huyJm_0'  # Vervang door je Supabase service key
    BUCKET_NAME = "pdf_files"  # De bucket waar je PDF's opslaat

supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)