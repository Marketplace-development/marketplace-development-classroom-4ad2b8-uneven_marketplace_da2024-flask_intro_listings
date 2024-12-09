import os

class Config:
    # Use DATABASE_URL from environment or hardcode for debugging
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres.rfgfcpljgfwblooetbms:CulinaryHeritage123ç@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True