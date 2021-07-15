"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
DEFAULT_IMAGE = 'https://i.imgur.com/2NFyNvK.jpeg'
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """user class for the blog website"""
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)
    
    first_name = db.Column(db.Text,
        nullable=False)
        
    last_name = db.Column(db.Text,
        nullable=False)
        
    img_url = db.Column(db.Text,
        nullable=False,
        default= DEFAULT_IMAGE)

    posts = db.relationship('Post',
        backref='author')


class Post(db.Model):
    """Creates class for user posts.
    Table creation/schema in blogly database."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, 
        primary_key=True,
        autoincrement=True)

    title = db.Column(db.Text,
        nullable=False)

    content = db.Column(db.Text,
        nullable=False)

    created_at = db.Column(db.DateTime, 
        nullable=False,
        default=datetime.now)

    user_id = db.Column(db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
        

