import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False,


class LocalDevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG =True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_PASSWORD_HASH = 'argon2'

     # ✅ EMAIL CONFIG
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "pratap.30m@gmail.com"
    MAIL_PASSWORD = "cbtbrwmidsicwmsk"   # ⚠️ NOT your normal password
    MAIL_DEFAULT_SENDER = "pratap.30m@gmail.com"

class ProductionConfig(BaseConfig):
    DEBUG = False