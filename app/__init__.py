from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Create the Flask application instance
app = Flask(__name__)

# Load the configuration from the Config class in config.py
app.config.from_object(Config)

# Create the SQLAlchemy database instance
db = SQLAlchemy(app)

# Create the database migration engine instance
migrate = Migrate(app, db)

# Create the Flask-Login instance
login = LoginManager(app)

# Set the login view for the application
login.login_view = 'login'

# Import the routes and models modules to complete the application setup
from app import routes, models