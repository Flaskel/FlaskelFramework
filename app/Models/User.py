from app.Database.database import db
from app.Models.Model import Model

class User(Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(150),nullable=False,unique=True)
    password = db.Column(db.String(255),nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
