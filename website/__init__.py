from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
import os
import logging
from config import Config

db = SQLAlchemy()  # Initialize the SQLAlchemy database instance
csrf = CSRFProtect()  # Initialize CSRF protection
cors = CORS()  # Initialize CORS

def create_App():  # Function to create and configure the Flask application
    app = Flask(__name__) 
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)  # Initialize the database with the app
    csrf.init_app(app)  # Initialize CSRF protection
    cors.init_app(app)  # Initialize CORS
    
    # Configure logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
        logging.info('Note App startup')

    from .views import views # Import the views blueprint
    from .auth import auth # Import the auth blueprint

    app.register_blueprint(views, url_prefix='/')  # Register the views blueprint
    app.register_blueprint(auth, url_prefix='/')  # Register the auth blueprint

    from . import models
    create_database(app)  # Create the database if it doesn't exist
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))
    
    return app

def create_database(app):  # Function to create the database if it doesn't exist
    if not os.path.exists('instance/database.db'):  # Check if the database file
        with app.app_context():
            db.create_all()
        print('Created Database') 