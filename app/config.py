class Config:
    SECRET_KEY = '87ee0a491f401698515db74dd38f5afd'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.wldgklgaamkrzpwsadkb:a&d.dbs.group23@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True    #niet vergeten uitzetten wanneer applicatie klaar is, enkel aanzetten tijdens ontwikkelingsfase
