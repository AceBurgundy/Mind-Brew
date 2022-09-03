class Config:
        # Ensure templates are auto-reloaded
    TEMPLATES_AUTO_RELOAD = True

    SECRET_KEY = 'completebutincomplete'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///reviewer.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configure session to use filesystem (instead of signed cookies)
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"