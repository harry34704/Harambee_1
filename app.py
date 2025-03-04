import os
import shutil
from flask import Flask, flash, redirect, render_template, request, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timedelta
import stripe
from twilio.rest import Client

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Configure the PostgreSQL database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Initialize API clients
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
twilio_client = Client(
    os.environ.get("TWILIO_ACCOUNT_SID"),
    os.environ.get("TWILIO_AUTH_TOKEN")
)

# Create necessary directories
static_assets_dir = os.path.join('static', 'attached_assets')
os.makedirs(static_assets_dir, exist_ok=True)
os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "documents"), exist_ok=True)
os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "leases"), exist_ok=True)

# Import models after db initialization
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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

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
        return redirect(url_for("apply")) # Redirect to application form after basic registration

    return render_template("auth/register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_admin:
        registered_students = Student.query.all()
        pending_applications = Student.query.filter_by(status="pending").all()
        maintenance_requests = MaintenanceRequest.query.order_by(MaintenanceRequest.created_at.desc()).all()
        return render_template(
            "dashboard/admin.html",
            registered_students=registered_students,
            pending_applications=pending_applications,
            maintenance_requests=maintenance_requests
        )
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

@app.route("/apply", methods=["GET", "POST"])
@login_required
def apply():
    if request.method == "POST":
        # Get form data
        guardian_name = request.form.get("guardian_name")
        guardian_phone = request.form.get("guardian_phone")

        # Get uploaded files
        id_doc = request.files.get("id_document")
        parent_id = request.files.get("parent_id")
        payslip = request.files.get("payslip")
        bank_statement = request.files.get("bank_statement")

        # Update student record
        student = Student.query.filter_by(user_id=current_user.id).first()
        student.guardian_name = guardian_name
        student.guardian_phone = guardian_phone
        student.status = "pending"

        # Save uploaded files
        if id_doc:
            filename = secure_filename(id_doc.filename)
            id_doc.save(os.path.join(app.config["UPLOAD_FOLDER"], "documents", filename))
            student.id_document = filename

        if parent_id:
            filename = secure_filename(parent_id.filename)
            parent_id.save(os.path.join(app.config["UPLOAD_FOLDER"], "documents", filename))
            student.parent_id = filename

        if payslip:
            filename = secure_filename(payslip.filename)
            payslip.save(os.path.join(app.config["UPLOAD_FOLDER"], "documents", filename))
            student.payslip = filename

        if bank_statement:
            filename = secure_filename(bank_statement.filename)
            bank_statement.save(os.path.join(app.config["UPLOAD_FOLDER"], "documents", filename))
            student.bank_statement = filename

        db.session.commit()
        flash("Application submitted successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("apply.html")

@app.route("/admin/applications")
@login_required
def admin_applications():
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("home"))

    applications = Student.query.filter_by(status="pending").all()
    return render_template("admin/applications.html", applications=applications)

@app.route("/admin/process_application/<int:student_id>", methods=["POST"])
@login_required
def process_application(student_id):
    if not current_user.is_admin:
        return {"error": "Access denied"}, 403

    student = Student.query.get_or_404(student_id)
    action = request.form.get("action")

    if action in ["approve", "reject", "hold"]:
        student.status = action
        db.session.commit()

        # Send SMS notification
        message = f"Your application has been {action}ed."
        if action == "hold":
            message = "Your application is on hold. Please check your email for required documents."

        try:
            from utils.sms import send_application_status
            send_application_status(student, action)
        except Exception as e:
            app.logger.error(f"SMS sending failed: {str(e)}")
            # Continue with the process even if SMS fails

        flash(f"Application {action}ed successfully!", "success")

    return redirect(url_for("admin_applications"))

@app.route("/view_document/<int:student_id>/<doc_type>")
@login_required
def view_document(student_id, doc_type):
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("home"))

    student = Student.query.get_or_404(student_id)
    document_path = None

    if doc_type == "id" and student.id_document:
        document_path = student.id_document
    elif doc_type == "parent_id" and student.parent_id:
        document_path = student.parent_id
    elif doc_type == "payslip" and student.payslip:
        document_path = student.payslip
    elif doc_type == "bank_statement" and student.bank_statement:
        document_path = student.bank_statement

    if document_path:
        return send_from_directory(os.path.join(app.config["UPLOAD_FOLDER"], "documents"), document_path)

    flash("Document not found.", "danger")
    return redirect(url_for("admin_applications"))


@app.route("/admin/view_student/<int:student_id>")
@login_required
def admin_view_student(student_id):
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("home"))

    student = Student.query.get_or_404(student_id)
    return render_template("admin/student_detail.html", student=student)

@app.route("/update_maintenance/<int:request_id>", methods=["POST"])
@login_required
def update_maintenance(request_id):
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("dashboard"))

    maintenance = MaintenanceRequest.query.get_or_404(request_id)
    new_status = request.form.get("status")
    if new_status in ["pending", "in_progress", "completed"]:
        maintenance.status = new_status
        if new_status == "completed":
            maintenance.resolved_at = datetime.utcnow()
        db.session.commit()
        flash("Maintenance request status updated.", "success")
    return redirect(url_for("dashboard"))

@app.route("/book_room", methods=["POST"])
@login_required
def book_room():
    if not current_user.is_authenticated:
        flash("Please login to book a room", "error")
        return redirect(url_for("login"))

    room_id = request.form.get("room_id")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    # Validate dates
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date < datetime.now().date():
            flash("Start date cannot be in the past", "error")
            return redirect(url_for("accommodation"))

        if end_date <= start_date:
            flash("End date must be after start date", "error")
            return redirect(url_for("accommodation"))
    except ValueError:
        flash("Invalid date format", "error")
        return redirect(url_for("accommodation"))

    # Get the room and check availability
    room = Accommodation.query.get_or_404(room_id)
    if not room.is_available:
        flash("This room is no longer available", "error")
        return redirect(url_for("accommodation"))

    # Create lease agreement
    student = Student.query.filter_by(user_id=current_user.id).first()
    lease = LeaseAgreement(
        student_id=student.id,
        room_number=room.room_number,
        start_date=start_date,
        end_date=end_date
    )

    # Update room availability
    room.is_available = False

    # Save changes
    db.session.add(lease)
    db.session.commit()

    flash("Room booked successfully! Please wait for admin approval.", "success")
    return redirect(url_for("dashboard"))

@app.route("/maintenance_request", methods=["POST"])
@login_required
def maintenance_request():
    description = request.form.get("description")
    if not description:
        flash("Please provide a description of the issue", "error")
        return redirect(url_for("dashboard"))

    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student or not student.room_number:
        flash("You must be assigned to a room to submit maintenance requests", "error")
        return redirect(url_for("dashboard"))

    maintenance = MaintenanceRequest(
        student_id=student.id,
        room_number=student.room_number,
        description=description
    )

    db.session.add(maintenance)
    db.session.commit()

    flash("Maintenance request submitted successfully", "success")
    return redirect(url_for("dashboard"))

@app.route("/request_leave", methods=["POST"])
@login_required
def request_leave():
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student or not student.room_number:
        flash("You must be assigned to a room to submit a leave request", "error")
        return redirect(url_for("dashboard"))

    # Calculate notice period
    leave_date = datetime.now().date()
    notice_period = leave_date + timedelta(days=30)  # 1 month notice

    # Update lease agreement
    lease = LeaseAgreement.query.filter_by(
        student_id=student.id,
        room_number=student.room_number
    ).order_by(LeaseAgreement.created_at.desc()).first()

    if lease:
        lease.end_date = notice_period
        db.session.commit()
        flash(f"Leave request submitted. Your notice period ends on {notice_period.strftime('%Y-%m-%d')}", "success")
    else:
        flash("No active lease found", "error")

    return redirect(url_for("dashboard"))

@app.route("/download_lease/<int:lease_id>")
@login_required
def download_lease(lease_id):
    lease = LeaseAgreement.query.get_or_404(lease_id)

    # Verify user has access to this lease
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not current_user.is_admin and (not student or lease.student_id != student.id):
        flash("Access denied", "error")
        return redirect(url_for("dashboard"))

    if not lease.pdf_file:
        flash("No lease agreement file available", "error")
        return redirect(url_for("dashboard"))

    return send_from_directory(
        os.path.join(app.config["UPLOAD_FOLDER"], "leases"),
        lease.pdf_file,
        as_attachment=True
    )

# Copy images from attached_assets to static/attached_assets
source_dir = 'attached_assets'
for image in ['pi4.jpg', 'pi5.jpg', 'pi6.jpg', 'pi7.jpg', 'pic1.jpg', 'pic2.jpg', 'pic_3.jpg']:
    source = os.path.join(source_dir, image)
    destination = os.path.join(static_assets_dir, image.replace(' ', '_'))
    if os.path.exists(source):
        shutil.copy2(source, destination)


def create_admin_user():
    admin_email = "admin@harambee.com"
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            email=admin_email,
            password=generate_password_hash("admin123"),  # Default password, should be changed
            is_admin=True
        )
        admin_profile = Admin(
            user=admin,
            name="System Admin"
        )
        db.session.add(admin)
        db.session.add(admin_profile)
        db.session.commit()
        print("Admin user created successfully!")

# Initialize database tables
with app.app_context():
    db.create_all()
    create_admin_user()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)