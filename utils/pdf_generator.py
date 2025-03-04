from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import os

def generate_lease_agreement(student, room, start_date, end_date):
    filename = f"lease_agreement_{student.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("uploads", "leases", filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "HARAMBEE ACCOMMODATION LEASE AGREEMENT")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, f"Student Name: {student.name}")
    c.drawString(50, 680, f"Room Number: {room.room_number}")
    c.drawString(50, 660, f"Start Date: {start_date}")
    c.drawString(50, 640, f"End Date: {end_date}")
    c.drawString(50, 620, f"Monthly Rent: R{room.price}")
    
    # Add terms and conditions
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 580, "Terms and Conditions:")
    
    c.setFont("Helvetica", 10)
    terms = [
        "1. Rent is due on the 1st of each month",
        "2. Maintenance requests must be submitted through the portal",
        "3. Keep common areas clean and tidy",
        "4. No unauthorized guests allowed",
        "5. Noise levels must be kept reasonable"
    ]
    
    y = 560
    for term in terms:
        c.drawString(50, y, term)
        y -= 20
    
    # Add signature lines
    c.drawString(50, 400, "Student Signature: _______________________")
    c.drawString(50, 380, "Date: _______________________")
    
    c.drawString(50, 320, "Administrator Signature: _______________________")
    c.drawString(50, 300, "Date: _______________________")
    
    c.save()
    return filename
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

def generate_lease_agreement(student, room, lease):
    """Generate a PDF lease agreement"""
    filename = f"lease_{student.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("uploads", "leases", filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "HARAMBEE STUDENT LIVING LEASE AGREEMENT")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, f"Student Name: {student.name}")
    c.drawString(50, 680, f"Room Number: {room.room_number}")
    c.drawString(50, 660, f"Start Date: {lease.start_date}")
    c.drawString(50, 640, f"End Date: {lease.end_date}")
    c.drawString(50, 620, f"Monthly Rent: R{room.price}")
    
    # Add terms and conditions
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 580, "Terms and Conditions:")
    
    c.setFont("Helvetica", 10)
    terms = [
        "1. Rent is due on the 1st of each month",
        "2. Maintenance requests must be submitted through the portal",
        "3. Keep common areas clean and tidy",
        "4. No unauthorized guests allowed",
        "5. Noise levels must be kept reasonable"
    ]
    
    y = 560
    for term in terms:
        c.drawString(50, y, term)
        y -= 20
    
    # Add signature lines
    c.drawString(50, 400, f"Student Signature: {student.name}")
    c.drawString(50, 380, f"Date: {lease.signature_date.strftime('%Y-%m-%d') if lease.signature_date else ''}")
    
    c.drawString(50, 320, "Administrator Signature: _______________________")
    c.drawString(50, 300, "Date: _______________________")
    
    c.save()
    
    return filename

def generate_invoice(student, room, lease):
    """Generate a PDF invoice"""
    filename = f"invoice_{student.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("uploads", "invoices", filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(250, 750, "INVOICE")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 720, "Harambee Student Living")
    c.setFont("Helvetica", 10)
    c.drawString(50, 705, "123 University Avenue")
    c.drawString(50, 690, "Johannesburg, South Africa")
    
    # Invoice details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, 720, "Invoice #:")
    c.drawString(400, 705, "Date:")
    c.drawString(400, 690, "Status:")
    
    c.setFont("Helvetica", 12)
    c.drawString(470, 720, f"INV-{lease.id}-{lease.created_at.strftime('%Y%m%d')}")
    c.drawString(470, 705, datetime.now().strftime("%Y-%m-%d"))
    c.drawString(470, 690, "PAID")
    
    # Student info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 650, "Invoice To:")
    c.setFont("Helvetica", 12)
    c.drawString(50, 635, student.name)
    c.drawString(50, 620, f"Room {lease.room_number}")
    
    # Line
    c.line(50, 600, 550, 600)
    
    # Items
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 580, "Description")
    c.drawString(450, 580, "Amount")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 560, f"Accommodation Fee - Room {lease.room_number} (First Month)")
    c.drawString(450, 560, f"R{room.price}")
    
    c.drawString(50, 540, "Security Deposit")
    c.drawString(450, 540, f"R{room.price}")
    
    # Line
    c.line(50, 520, 550, 520)
    
    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, 500, "Total:")
    c.drawString(450, 500, f"R{room.price * 2}")
    
    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(50, 100, "Payment Method: Bank Transfer")
    c.drawString(50, 85, "Bank: Standard Bank")
    c.drawString(50, 70, "Account: 123456789")
    c.drawString(50, 55, f"Reference: STU{student.id}")
    
    c.save()
    
    return filename
