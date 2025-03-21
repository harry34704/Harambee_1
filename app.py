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
from twilio.rest import Client

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
login_manager.login_view = "login"

# Initialize API clients
twilio_client = None

def register_app_components(app):
    global twilio_client
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    
    # Initialize API clients if environment variables are available
    twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    
    if twilio_account_sid and twilio_auth_token:
        twilio_client = Client(twilio_account_sid, twilio_auth_token)
    
    # Create necessary directories
    static_assets_dir = os.path.join('static', 'attached_assets')
    os.makedirs(static_assets_dir, exist_ok=True)
    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "documents"), exist_ok=True)
    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "leases"), exist_ok=True)
    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "payments"), exist_ok=True)
    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "invoices"), exist_ok=True)
    
    # Import models after db initialization
    from models import User, Student, Admin, Accommodation, LeaseAgreement, MaintenanceRequest
    
    # Register routes
    register_routes(app)
    
    # Copy images from attached_assets to static/attached_assets
    copy_asset_images(static_assets_dir)
    
    # Initialize database tables and create admin user
    with app.app_context():
        db.create_all()
        create_admin_user()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

def create_admin_user():
    from models import User, Admin
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

def copy_asset_images(static_assets_dir):
    source_dir = 'attached_assets'
    for image in ['pi4.jpg', 'pi5.jpg', 'pi6.jpg', 'pi7.jpg', 'pic1.jpg', 'pic2.jpg', 'pic_3.jpg']:
        source = os.path.join(source_dir, image)
        destination = os.path.join(static_assets_dir, image.replace(' ', '_'))
        if os.path.exists(source):
            shutil.copy2(source, destination)

def register_routes(app):
    # Routes
    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            from models import User
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
            id_number = request.form.get("id_number")
            student_number = request.form.get("student_number")
            
            from models import User, Student
            if User.query.filter_by(email=email).first():
                flash("Email already registered", "danger")
                return redirect(url_for("register"))

            user = User(
                email=email,
                password=generate_password_hash(password),
                is_admin=False
            )
            student = Student(
                name=name,
                phone=phone,
                id_number=id_number,
                student_number=student_number,
                user=user
            )

            db.session.add(user)
            db.session.add(student)
            db.session.commit()

            login_user(user)
            return redirect(url_for("academic_info")) # Redirect to academic info page after basic registration

        return render_template("auth/register.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():
        from models import Student, MaintenanceRequest, LeaseAgreement
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
            lease_agreements = LeaseAgreement.query.filter_by(student_id=student.id).all()
            maintenance_requests = MaintenanceRequest.query.filter_by(student_id=student.id).all()
            return render_template("dashboard/student.html", student=student, lease_agreements=lease_agreements, maintenance_requests=maintenance_requests)

    @app.route("/accommodation")
    def accommodation():
        from models import Accommodation
        rooms = Accommodation.query.all()
        return render_template("accommodation.html", rooms=rooms)

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    @app.route("/academic_info", methods=["GET", "POST"])
    @login_required
    def academic_info():
        from models import Student
        
        # Get current student's academic info if it exists
        student = Student.query.filter_by(user_id=current_user.id).first()
        
        if request.method == "POST":
            institution = request.form.get("institution")
            if institution == "Other":
                institution = request.form.get("other_institution")
            campus = request.form.get("campus")
            course = request.form.get("course")
            year_of_study = request.form.get("year_of_study")
            
            if not student:
                student = Student(user_id=current_user.id)
                db.session.add(student)
            
            student.institution = institution
            student.campus = campus
            student.course = course
            student.year_of_study = year_of_study
            
            db.session.commit()
            flash("Academic information saved successfully!", "success")
            return redirect(url_for("apply"))
        
        return render_template("academic_info.html", student=student)

    @app.route("/save_academic_info", methods=["POST"])
    @login_required
    def save_academic_info():
        from models import Student
        
        # Get form data
        institution = request.form.get("institution")
        if institution == "Other":
            institution = request.form.get("other_institution")
        campus = request.form.get("campus")
        course = request.form.get("course")
        year_of_study = request.form.get("year_of_study")
        
        # Update student record
        student = Student.query.filter_by(user_id=current_user.id).first()
        student.institution = request.form.get("institution")
        student.campus = request.form.get("campus")
        course = request.form.get("course")
        course = request.form.get("course")
        student.course = request.form.get("course")
        student.year_of_study = request.form.get("year_of_study")
        
        db.session.commit()
        flash("Academic information saved successfully!", "success")
        return redirect(url_for("apply"))
    
    @app.route('/apply', methods=['GET', 'POST'])
    @login_required
    def apply():
        from models import Accommodation, Student
        
        student = Student.query.filter_by(user_id=current_user.id).first()
        
        if not student.institution:
            flash("Please complete your academic information first", "warning")
            return redirect(url_for("academic_info"))
        
        if request.method == "POST":
            try:
                # Handle file uploads
                files = {
                    'id_document': request.files.get('id_document'),
                    'parent_id': request.files.get('parent_id'),
                    'proof_of_registration': request.files.get('proof_of_registration'),
                    'bank_statement': request.files.get('bank_statement')
                }
                
                # Validate all required files are present
                for key, file in files.items():
                    if not file:
                        flash(f"Missing required document: {key.replace('_', ' ').title()}", "danger")
                        return redirect(request.url)
                
                # Process and save files
                for key, file in files.items():
                    if file:
                        filename = secure_filename(f"{key}_{student.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}{os.path.splitext(file.filename)[1]}")
                        file.save(os.path.join(app.config["UPLOAD_FOLDER"], "documents", filename))
                        setattr(student, key, filename)
                
                # Update student information
                student.accommodation_preference = request.form.get("accommodation_preference")
                student.guardian_name = request.form.get("guardian_name")
                student.guardian_phone = request.form.get("guardian_phone")
                student.guardian_id_number = request.form.get("guardian_id_number")
                student.guardian_street_address = request.form.get("guardian_street_address")
                student.guardian_city = request.form.get("guardian_city")
                student.status = "pending"
                
                db.session.commit()
                
                # Send notification
                try:
                    from utils.sms import send_application_notification
                    send_application_notification(student)
                except Exception as e:
                    app.logger.error(f"Failed to send notification: {str(e)}")
                
                flash("Application submitted successfully! We will review it shortly.", "success")
                return redirect(url_for("dashboard"))
                
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Application submission failed: {str(e)}")
                flash("An error occurred while submitting your application. Please try again.", "danger")
                return redirect(request.url)
        
        accommodations = Accommodation.query.filter_by(is_available=True).all()
        return render_template('apply.html', accommodations=accommodations, student=student)

    @app.route("/admin/applications")
    @login_required
    def admin_applications():
        if not current_user.is_admin:
            flash("Access denied.", "danger")
            return redirect(url_for("home"))
        from models import Student
        # Only show applications from Highlands College
        applications = Student.query.filter_by(status="pending", institution="Highlands College").all()
        return render_template("admin/applications.html", applications=applications)

    @app.route("/admin/process_application/<int:student_id>", methods=["POST"])
    @login_required
    def process_application(student_id):
        if not current_user.is_admin:
            return
        from models import Student, Accommodation, LeaseAgreement
        from datetime import datetime, timedelta
        student = Student.query.get_or_404(student_id)
        action = request.form.get("action")

        if action in ["approve", "reject", "hold", "partial_approve"]:
            student.status = action
            
            if action in ["approve", "partial_approve"]:
                lease = LeaseAgreement(
                    student_id=student.id,
                    room_number=student.accommodation_preference,
                    start_date=datetime.now().date(),
                    end_date=datetime.now().date() + timedelta(days=365),
                    status="pending"
                )
                db.session.add(lease)
            
            db.session.commit()

            message = f"Your application has been {action}ed."
            if action == "hold":
                message = "Your application is on hold. Please contact admin for more details."
            elif action == "partial_approve":
                message = "Your application is partially approved. Please review the details."
            elif action == "approve":
                message = "Your application is approved. Please sign the lease agreement."

            try:
                # Send SMS notification
                if twilio_client:
                    twilio_client.messages.create(
                        body=message,
                        from_=os.environ.get("TWILIO_PHONE_NUMBER"),
                        to=student.phone
                    )
            except Exception as e:
                app.logger.error(f"SMS sending failed: {str(e)}")

            flash(f"Application {action}ed successfully!", "success")

        return redirect(url_for("admin_applications"))

    @app.route("/view_document/<int:student_id>/<doc_type>")
    @login_required
    def view_document(student_id, doc_type):
        if not current_user.is_admin:
            flash("Access denied.", "danger")
            return redirect(url_for("home"))
        from models import Student
        student = Student.query.get_or_404(student_id)
        document_path = None

        if doc_type == "id" and student.id_document:
            document_path = student.id_document
        elif doc_type == "parent_id" and student.parent_id:
            document_path = student.parent_id
        elif doc_type == "proof_of_registration" and student.proof_of_registration:
            document_path = student.proof_of_registration
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
        from models import Student
        student = Student.query.get_or_404(student_id)
        return render_template("admin/student_detail.html", student=student)

    @app.route("/update_maintenance/<int:request_id>", methods=["POST"])
    @login_required
    def update_maintenance(request_id):
        if not current_user.is_admin:
            flash("Access denied.", "danger")
            return redirect(url_for("dashboard"))
        from models import MaintenanceRequest
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
        from models import Accommodation, Student, LeaseAgreement
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
            end_date=end_date,
            status="pending"
        )

        # Update room availability (not updating yet until lease is signed and payment verified)
        # room.is_available = False

        # Save changes
        db.session.add(lease)
        db.session.commit()

        flash("Room booking initiated. Please sign your lease agreement.", "success")
        return redirect(url_for("sign_lease", lease_id=lease.id))

    @app.route("/lease/<int:lease_id>/sign", methods=["GET", "POST"])
    @login_required
    def sign_lease(lease_id):
        from models import LeaseAgreement, Student, Accommodation
        lease = LeaseAgreement.query.get_or_404(lease_id)
        student = Student.query.filter_by(user_id=current_user.id).first()
        
        if student.id != lease.student_id and not current_user.is_admin:
            flash("Access denied", "danger")
            return redirect(url_for("dashboard"))
        
        room = Accommodation.query.filter_by(room_number=lease.room_number).first()
        
        if request.method == "POST":
            signature = request.form.get("signature")
            guardian_signature = request.form.get("guardian_signature")
            agree = request.form.get("agree")
            
            if agree and signature:
                lease.status = "signed_by_student"
                lease.student_signature = signature
                lease.guardian_signature = guardian_signature
                lease.student_signature_date = datetime.utcnow()
                db.session.commit()
                flash("Lease agreement signed successfully!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("You must agree to the terms and provide your signature.", "danger")
        
        return render_template("lease_sign.html", lease=lease, student=student, room=room)
        
    @app.route("/admin/lease/<int:lease_id>/sign", methods=["POST"])
    @login_required
    def admin_sign_lease(lease_id):
        if not current_user.is_admin:
            flash("Access denied.", "danger")
            return redirect(url_for("dashboard"))
            
        from models import LeaseAgreement, Student, Accommodation
        lease = LeaseAgreement.query.get_or_404(lease_id)
        student = Student.query.get(lease.student_id)
        room = Accommodation.query.filter_by(room_number=lease.room_number).first()
        
        signature = request.form.get("signature")
        agree = request.form.get("agree")
        
        if agree and signature:
            lease.status = "fully_signed"
            lease.admin_signature = signature
            lease.admin_signature_date = datetime.utcnow()
            
            # Generate the PDF lease agreement with both signatures
            from utils.pdf_generator import generate_lease_agreement
            filename = generate_lease_agreement(student, room, lease)
            lease.pdf_file = filename
            
            db.session.commit()
            
            flash("Lease agreement fully signed! Student can now proceed to payment.", "success")
            
            # Send notification to student
            try:
                from utils.sms import send_sms_notification
                message = f"Hello {student.name}, your lease agreement for Room {room.room_number} has been signed by the administrator. You can now proceed to payment."
                send_sms_notification(student.phone, message)
            except Exception as e:
                app.logger.error(f"SMS sending failed: {str(e)}")
                
            return redirect(url_for("admin_leases"))
        else:
            flash("You must agree to the terms and provide your signature.", "danger")
            return redirect(url_for("admin_sign_lease", lease_id=lease.id))
            
    @app.route("/admin/lease/<int:lease_id>/view", methods=["GET"])
    @login_required
    def admin_view_lease(lease_id):
        if not current_user.is_admin:
            flash("Access denied.", "danger")
            return redirect(url_for("dashboard"))
            
        from models import LeaseAgreement, Student, Accommodation
        lease = LeaseAgreement.query.get_or_404(lease_id)
        student = Student.query.get(lease.student_id)
        room = Accommodation.query.filter_by(room_number=lease.room_number).first()
        
        return render_template("lease_sign.html", lease=lease, student=student, room=room)

    @app.route("/lease/<int:lease_id>/payment", methods=["GET", "POST"])
    @login_required
    def upload_payment_proof(lease_id):
        from models import LeaseAgreement, Student, Accommodation
        lease = LeaseAgreement.query.get_or_404(lease_id)
        student = Student.query.filter_by(user_id=current_user.id).first()
        
        # Verify this lease belongs to the current user
        if student.id != lease.student_id and not current_user.is_admin:
            flash("Access denied", "danger")
            return redirect(url_for("dashboard"))
        
        # Check if lease is in the correct state
        if lease.status != "signed":
            flash("Please sign your lease agreement first.", "warning")
            return redirect(url_for("sign_lease", lease_id=lease.id))
        
        # Get room information
        room = Accommodation.query.filter_by(room_number=lease.room_number).first()
        
        if request.method == "POST":
            # Check if the post request has the file part
            if 'payment_proof' not in request.files:
                flash('No file part', 'danger')
                return redirect(request.url)
            
            file = request.files['payment_proof']
            
            # If user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)
            
            if file:
                # Use the original file extension instead of forcing PDF
                ext = os.path.splitext(file.filename)[1]
                filename = secure_filename(f"payment_{lease.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}")
                
                # Make sure the directory exists
                os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "payments"), exist_ok=True)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], "payments", filename))
                
                lease.payment_proof = filename
                lease.status = "payment_pending"
                db.session.commit()
                
                # Notify admin of new payment proof
                flash("Payment proof uploaded successfully! Please wait for verification.", "success")
                return redirect(url_for("dashboard"))
        
        return render_template("payment_proof.html", lease=lease, student=student, room=room)

    @app.route("/admin/verify_payment/<int:lease_id>", methods=["POST"])
    @login_required
    def verify_payment(lease_id):
        if not current_user.is_admin:
            flash("Access denied.", "danger")
            return redirect(url_for("dashboard"))
        from models import LeaseAgreement, Student, Accommodation
        lease = LeaseAgreement.query.get_or_404(lease_id)
        action = request.form.get("action")
        
        if action == "approve":
            student = Student.query.get(lease.student_id)
            room = Accommodation.query.filter_by(room_number=lease.room_number).first()
            
            lease.payment_verified = True
            lease.status = "active"
            
            from utils.pdf_generator import generate_invoice
            invoice_filename = generate_invoice(student, room, lease)
            lease.invoice_file = invoice_filename
            
            room.is_available = False
            student.room_number = room.room_number
            
            db.session.commit()
            
            try:
                # Send notification to student
                pass
            except Exception as e:
                pass
            
            flash("Payment verified and invoice generated successfully!", "success")
        elif action == "reject":
            lease.status = "signed"
            db.session.commit()
            flash("Payment rejected. Student will need to re-upload payment proof.", "warning")
        
        return redirect(url_for("admin_leases"))

    @app.route("/admin/leases")
    @login_required
    def admin_leases():
        if not current_user.is_admin:
            flash("Access denied.", "danger")
            return redirect(url_for("dashboard"))
        from models import LeaseAgreement
        leases = LeaseAgreement.query.order_by(LeaseAgreement.created_at.desc()).all()
        return render_template("admin/leases.html", leases=leases)

    @app.route("/invoice/<int:lease_id>")
    @login_required
    def view_invoice(lease_id):
        from models import LeaseAgreement, Student, Accommodation
        lease = LeaseAgreement.query.get_or_404(lease_id)
        student = Student.query.filter_by(user_id=current_user.id).first()
        
        # Verify access
        if not current_user.is_admin and (not student or lease.student_id != student.id):
            flash("Access denied", "danger")
            return redirect(url_for("dashboard"))
        
        # Check if invoice exists
        if not lease.invoice_file:
            flash("Invoice not yet generated", "warning")
            return redirect(url_for("dashboard"))
        
        room = Accommodation.query.filter_by(room_number=lease.room_number).first()
        now = datetime.now()
        
        return render_template("invoice.html", lease=lease, student=student, room=room, now=now)

    @app.route("/download_invoice/<int:lease_id>")
    @login_required
    def download_invoice(lease_id):
        from models import LeaseAgreement, Student
        lease = LeaseAgreement.query.get_or_404(lease_id)
        student = Student.query.filter_by(user_id=current_user.id).first()
        
        # Verify access
        if not current_user.is_admin and (not student or lease.student_id != student.id):
            flash("Access denied", "danger")
            return redirect(url_for("dashboard"))
        
        if not lease.invoice_file:
            flash("Invoice not yet generated", "warning")
            return redirect(url_for("dashboard"))
        
        return send_from_directory(
            os.path.join(app.config["UPLOAD_FOLDER"], "invoices"),
            lease.invoice_file,
            as_attachment=True
        )

    @app.route("/view_payment_proof/<int:lease_id>")
    @login_required
    def view_payment_proof(lease_id):
        from models import LeaseAgreement, Student
        lease = LeaseAgreement.query.get_or_404(lease_id)
        
        # Verify access
        student = Student.query.filter_by(user_id=current_user.id).first()
        if not current_user.is_admin and (not student or lease.student_id != student.id):
            flash("Access denied", "danger")
            return redirect(url_for("dashboard"))
        
        if not lease.payment_proof:
            flash("No payment proof uploaded", "warning")
            return redirect(url_for("dashboard"))
        
        return send_from_directory(
            os.path.join(app.config["UPLOAD_FOLDER"], "payments"),
            lease.payment_proof
        )

    @app.route("/maintenance_request", methods=["POST"])
    @login_required
    def maintenance_request():
        from models import Student, MaintenanceRequest
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
        from models import Student, LeaseAgreement
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
        from models import LeaseAgreement, Student
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

    @app.route("/resume_application")
    @login_required
    def resume_application():
        from models import Student
        student = Student.query.filter_by(user_id=current_user.id).first()
        if student and student.status == "incomplete":
            return redirect(url_for("apply"))
        flash("No incomplete application found.", "warning")
        return redirect(url_for("dashboard"))

    @app.route("/api/check_application_state", methods=["GET"])
    @login_required
    def check_application_state():
        from models import Student
        student = Student.query.filter_by(user_id=current_user.id).first()
        if student:
            return {
                "status": student.status,
                "accommodation_preference": student.accommodation_preference,
                "guardian_name": student.guardian_name,
                "guardian_phone": student.guardian_phone,
                "guardian_id_number": student.guardian_id_number,
                "guardian_street_address": student.guardian_street_address,
                "guardian_city": student.guardian_city,
                "id_document": student.id_document,
                "parent_id": student.parent_id,
                "proof_of_registration": student.proof_of_registration,
                "bank_statement": student.bank_statement
            }, 200
        return {"error": "Student not found"}, 404

    @app.context_processor
    def inject_context():
        return {
            'current_user': current_user
        }
