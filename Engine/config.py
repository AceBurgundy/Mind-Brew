from dotenv import load_dotenv
import os
load_dotenv()


class Config:
    # Ensure templates are auto-reloaded
    TEMPLATES_AUTO_RELOAD = True

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///reviewer.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configure session to use filesystem (instead of signed cookies)
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    # Email

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 2525
    MAIL_USERNAME = os.getenv("MAIL_USER")
    MAIL_PASSWORD = os.getenv("MAIL_PASS")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
