from flask import Flask
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from app.database.database import db
from app.Command.MakeModel import make_model
from app import Models  # ensure models are registered


# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- APP INIT ----------------
app = Flask(__name__)

# ---------------- CONFIG ----------------
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ---------------- INIT EXTENSIONS ----------------
db.init_app(app)
migrate = Migrate(app, db, directory="app/Database/Migrations")

# ---------------- CLI COMMANDS ----------------
app.cli.add_command(make_model)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)