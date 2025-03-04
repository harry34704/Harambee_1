import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import stripe
from twilio.rest import Client

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///harambee.db"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
twilio_client = Client(
    os.environ.get("TWILIO_ACCOUNT_SID"),
    os.environ.get("TWILIO_AUTH_TOKEN")
)

db.init_app(app)

from models import User, Student, Admin, Accommodation, LeaseAgreement, MaintenanceRequest

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid credentials")
    return render_template("auth/login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for("register"))
            
        user = User(
            email=email,
            password=generate_password_hash(password),
            is_admin=False
        )
        student = Student(
            name=name,
            phone=phone,
            user=user
        )
        
        db.session.add(user)
        db.session.add(student)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for("dashboard"))
        
    return render_template("auth/register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_admin:
        pending_applications = Student.query.filter_by(status="pending").all()
        return render_template("dashboard/admin.html", applications=pending_applications)
    else:
        student = Student.query.filter_by(user_id=current_user.id).first()
        return render_template("dashboard/student.html", student=student)

@app.route("/accommodation")
def accommodation():
    rooms = Accommodation.query.all()
    return render_template("accommodation.html", rooms=rooms)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
