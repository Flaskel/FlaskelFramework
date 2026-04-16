from app.Database.database import db
from .Model import Model
from sqlalchemy.sql import func
from uuid import uuid4
from flask_login import UserMixin

class User(Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.String(36),primary_key=True, default=uuid4)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(150),nullable=False,unique=True)
    mobile = db.Column(db.String(15),nullable=True)
    password = db.Column(db.String(255),nullable=False)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())