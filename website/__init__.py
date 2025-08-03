from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()  # Initialize the SQLAlchemy database instance
DB_NAME = 'database.db'  # Database file name

def create_App():  # Function to create and configure the Flask application
    app = Flask(__name__) 
    app.config['SECRET_KEY'] = 'ufuhndunvjieme veivimeicmic' # Example secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Database URI
    db.init_app(app)  # Initialize the database with the app

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
    if not path.exists('website/' + DB_NAME):  # Check if the database file
        with app.app_context():
            db.create_all()
        print('Created Database') 