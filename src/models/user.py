from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Smartlink(db.Model):
    __tablename__ = 'smartlinks'
    
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    views = db.Column(db.Integer, default=0, nullable=False)
    clicks = db.Column(db.Integer, default=0, nullable=False)
    
    # Nouveaux champs pour la page de destination personnalisable
    landing_page_title = db.Column(db.String(255), nullable=True)
    landing_page_subtitle = db.Column(db.String(255), nullable=True)
    cover_image_url = db.Column(db.Text, nullable=True)
    platforms_data = db.Column(db.Text, nullable=True)  # JSON string
    embed_url = db.Column(db.Text, nullable=True)
    long_description = db.Column(db.Text, nullable=True)
    social_sharing_enabled = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f'<Smartlink {self.id}>'

    def get_platforms(self):
        """Retourne les données des plateformes sous forme de liste de dictionnaires"""
        if self.platforms_data:
            try:
                return json.loads(self.platforms_data)
            except json.JSONDecodeError:
                return []
        return []

    def set_platforms(self, platforms_list):
        """Définit les données des plateformes à partir d'une liste de dictionnaires"""
        self.platforms_data = json.dumps(platforms_list)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'views': self.views,
            'clicks': self.clicks,
            'landing_page_title': self.landing_page_title,
            'landing_page_subtitle': self.landing_page_subtitle,
            'cover_image_url': self.cover_image_url,
            'platforms': self.get_platforms(),
            'embed_url': self.embed_url,
            'long_description': self.long_description,
            'social_sharing_enabled': self.social_sharing_enabled
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

