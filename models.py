from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Changed from default 'user' to avoid PostgreSQL keyword conflict
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Updated foreign key reference
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    guardian_name = db.Column(db.String(100))
    guardian_phone = db.Column(db.String(20))
    room_number = db.Column(db.String(10))
    status = db.Column(db.String(20), default="pending")  # pending, approved, rejected
    id_document = db.Column(db.String(255))
    parent_id = db.Column(db.String(255))
    payslip = db.Column(db.String(255))
    bank_statement = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='student', uselist=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Updated foreign key reference
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='admin', uselist=False)

class Accommodation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    room_type = db.Column(db.String(50))  # single, double, etc.
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Using Numeric for currency
    is_available = db.Column(db.Boolean, default=True)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LeaseAgreement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    room_number = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    pdf_file = db.Column(db.String(255))
    status = db.Column(db.String(20), default="pending")  # pending, signed_by_student, awaiting_admin_signature, fully_signed, payment_pending, payment_verified, active, completed
    payment_proof = db.Column(db.String(255))
    payment_verified = db.Column(db.Boolean, default=False)
    invoice_file = db.Column(db.String(255))
    student_signature = db.Column(db.String(255))
    guardian_signature = db.Column(db.String(255))
    admin_signature = db.Column(db.String(255))
    student_signature_date = db.Column(db.DateTime)
    admin_signature_date = db.Column(db.DateTime)
    signature_ip = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    student = db.relationship('Student', backref='lease_agreements')

class MaintenanceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    room_number = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    student = db.relationship('Student', backref='maintenance_requests')