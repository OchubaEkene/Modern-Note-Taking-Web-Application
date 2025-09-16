#!/usr/bin/env python3
"""
Database migration script for the Note-Storing Flask Web App.
This script recreates the database with the latest schema.
"""

from website import create_App, db
import os

def migrate_database():
    """Recreate the database with the latest schema."""
    app = create_App()
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("Dropped all existing tables")
        
        # Create all tables with new schema
        db.create_all()
        print("Created new database with updated schema")
        
        print("Database migration completed successfully!")

if __name__ == '__main__':
    migrate_database()
