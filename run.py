from flask import Flask, render_template, request, redirect, url_for, flash
from app.Command.MakeModel import make_model
from flask_migrate import Migrate
from app.Database.database import db
from dotenv import load_dotenv
from app.Models import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import os

load_dotenv()

app = Flask(__name__, static_folder="app/Resources/assets", template_folder="app/Resources/view")

# -----------------------------
# DATABASE CONFIG (DYNAMIC)
# -----------------------------
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")

app.config["SQLALCHEMY_DATABASE_URI"] = (f"{DB_DRIVER}+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# -----------------------------
# INIT
# -----------------------------
db.init_app(app)
migrate = Migrate(app, db, directory="app/Database/Migrations")


# -----------------------------
# Models Import
# -----------------------------
from app import Models


# -----------------------------
# LOAD MODELS
# -----------------------------
app.cli.add_command(make_model)

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("home.html")

@app.route("/dashboard", methods=["GET"], strict_slashes=False)
@login_required
def dashboard():
    return render_template("index.html")

@app.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("profile.html")

@app.route("/profile/update", methods=["POST"])
@login_required
def update_profile():
    name = request.form.get("name")
    email = request.form.get("email")
    mobile = request.form.get("mobile")

    user = current_user

    user.name = name
    user.email = email
    user.mobile = mobile

    db.session.commit()

    flash("Profile updated successfully", "success")
    return redirect(url_for("profile"))

@app.route("/profile/password", methods=["POST"])
@login_required
def update_password():
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    user = current_user

    if not check_password_hash(user.password, current_password):
        flash("Current password is incorrect", "error")
        return redirect(url_for("profile"))

    if new_password != confirm_password:
        flash("New password and confirm password do not match", "error")
        return redirect(url_for("profile"))

    user.password = generate_password_hash(new_password)
    db.session.commit()

    flash("Password updated successfully", "success")
    return redirect(url_for("profile"))

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All required fields must be filled", "error")
            return redirect(url_for("sign_up"))

        user = User.create(
            name=name,
            email=email,
            mobile=mobile,
            password=password,
            status=1
        )

        remember = request.form.get("remember") == "1"

        login_user(user, remember=remember)

        return redirect(url_for("dashboard"))

    return render_template("sign-up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not found", "error")
            return redirect(url_for("login"))

        if not check_password_hash(user.password, password):
            flash("Incorrect password", "error")
            return redirect(url_for("login"))
        
        remember = request.form.get("remember") == "1"

        login_user(user, remember=remember)
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/users")
@login_required
def users_list():
    if request.args.get("deleted"):
        flash("User deleted successfully", "success")   
    users = User.query.all()

    users_data = [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "mobile": u.mobile,
            "status": True if u.status == 1 else False
        } for u in users
    ]

    return render_template("users.html", users=users_data)

@app.route("/users/create", methods=["GET", "POST"])
@login_required
def create_user():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All required fields must be filled", "error")
            return redirect(url_for("create_user"))

        User.create(
            name=name,
            email=email,
            mobile=mobile,
            password=password,
            status=1
        )

        flash("User created successfully", "success")
        return redirect(url_for("users_list"))

    return render_template("create-user.html")

@app.route("/users/edit/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):

    user = User.query.get(user_id)

    if not user:
        flash("User not found", "error")
        return redirect(url_for("users_list"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        mobile = request.form.get("mobile")

        if not name or not email:
            flash("Name and Email are required", "error")
            return redirect(url_for("edit_user", user_id=user_id))

        user.name = name
        user.email = email
        user.mobile = mobile

        db.session.commit()

        flash("User updated successfully", "success")
        return redirect(url_for("users_list"))

    return render_template("edit-user.html", user=user)

@app.route("/users/toggle/<user_id>", methods=["POST"])
@login_required
def toggle_user_status(user_id):
    user = User.query.get(user_id)

    if not user:
        flash("User not found", "error")
        return redirect(url_for("users_list"))

    user.status = not user.status
    db.session.commit()

    if user.status:
        flash(f"{user.name} is activated", "success")
    else:
        flash(f"{user.name} is deactivated", "success")

    return redirect(url_for("users_list"))

@app.route("/users/delete/<user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return {"success": False, "message": "User not found"}, 404

    db.session.delete(user)
    db.session.commit()

    return {"success": True}

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
