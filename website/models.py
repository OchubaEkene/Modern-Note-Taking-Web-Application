from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import json

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), default='General')
    tags = db.Column(db.Text)  # JSON string of tags
    is_favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def set_tags(self, tags_list):
        """Set tags from a list"""
        self.tags = json.dumps(tags_list)
    
    def get_tags(self):
        """Get tags as a list"""
        if self.tags:
            return json.loads(self.tags)
        return []
    
    def to_dict(self):
        """Convert note to dictionary for API responses"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'tags': self.get_tags(),
            'is_favorite': self.is_favorite,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Define the User model for the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True))
    is_active = db.Column(db.Boolean, default=True)
    notes = db.relationship('Note', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def get_full_name(self):
        """Get user's full name"""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name