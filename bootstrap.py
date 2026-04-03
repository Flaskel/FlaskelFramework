from app import app as flask_app
from orm import db
import models

flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(flask_app)

with flask_app.app_context():
    db.create_all()
    