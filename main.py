from flask import Flask
from app import Models
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from app.Database.database import db
from app.Command.MakeModel import make_model
from urllib.parse import quote_plus


app = Flask("__name__")

# ---------------- CONFIG ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.getenv("DB_USER")}:{quote_plus(os.getenv("DB_PASSWORD", ""))}@{os.getenv("DB_HOST", "localhost")}:{os.getenv("DB_PORT", "3306")}/{os.getenv("DB_NAME")}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ------------------ INIT ------------------
db.init_app(app)
migrate = Migrate(app, db, directory="app/Database/Migrations")

app.cli.add_command(make_model)

if __name__ == "__main__":
    app.run(debug=True)