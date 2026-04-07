from flask import Flask, render_template
from app import Models
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from app.Database.database import db
from app.Command.MakeModel import make_model
# from urllib.parse import quote_plus

load_dotenv()
app = Flask(__name__,static_folder="app/Resources", template_folder="app/Resources/view")

# ---------------- CONFIG ----------------
DB_DRIVER=os.getenv('DB_DRIVER')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_NAME=os.getenv('DB_NAME')


app.config["SQLALCHEMY_DATABASE_URI"] = f"{DB_DRIVER}+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ------------------ INIT ------------------
db.init_app(app)
migrate = Migrate(app, db, directory="app/Database/Migrations")

app.cli.add_command(make_model)

# ------------------ ROUTES ------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign-up")
def sign_up():
    return render_template("sign-up.html")

@app.route("/sign-in")
def sign_in():
    return render_template("sign-in.html")

@app.route("/password-reset")
@app.route("/auth-boxed-password-reset.html")
@app.route("/auth-cover-password-reset.html")
def password_reset():
    return render_template("password-reset.html")

@app.route("/tables")
def tables():
    return render_template("tables.html")

@app.route("/forms")
def forms():
    return render_template("forms.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
