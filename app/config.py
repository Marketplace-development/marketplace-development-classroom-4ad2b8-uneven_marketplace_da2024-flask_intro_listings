import os

class Config:
    # Database connection string
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres.rfgfcpljgfwblooetbms:CulinaryHeritage123è@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
