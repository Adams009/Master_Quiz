import secrets

class Config:
    SECRET_KEY = secrets.token_hex(32)  # This is need for session security(secure session)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_master.db'  # SQLite database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for better performance

