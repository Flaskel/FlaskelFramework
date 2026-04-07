from database.database import db
from Models.model import Model
from datetime import datetime


class User(Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(150), nullable=False, unique=True, index=True)

    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)

    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

    