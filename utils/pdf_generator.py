
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import inch
from datetime import datetime
import os

def generate_lease_agreement(student, room, start_date, end_date):
    """Generate a PDF lease agreement"""
    filename = f"lease_agreement_{student.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("uploads", "leases", filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "HARAMBEE STUDENT ACCOMMODATION LEASE AGREEMENT")
    
    # Student and Room Information
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Student Name: {student.name}")
    c.drawString(50, height - 120, f"Room Number: {room.room_number}")
    c.drawString(50, height - 140, f"Start Date: {start_date}")
    c.drawString(50, height - 160, f"End Date: {end_date}")
    c.drawString(50, height - 180, f"Monthly Rent: R{room.price}")
    
    # Terms and Conditions
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 220, "Terms and Conditions:")
    
    c.setFont("Helvetica", 10)
    terms = [
        "1. Rent is due on the 1st of each month.",
        "2. A security deposit equal to one month's rent is required.",
        "3. Maintenance requests must be submitted through the portal.",
        "4. Common areas must be kept clean and tidy.",
        "5. No unauthorized guests are allowed overnight.",
        "6. Noise levels must be kept reasonable, especially between 10 PM and 7 AM.",
        "7. Smoking is not permitted inside the building.",
        "8. Pets are not allowed unless specifically authorized.",
        "9. Damage to property beyond normal wear and tear will be charged to the tenant.",
        "10. 30 days' notice is required for lease termination."
    ]
    
    y = height - 240
    for term in terms:
        c.drawString(50, y, term)
        y -= 20
    
    # Payment Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 20, "Payment Information:")
    c.setFont("Helvetica", 10)
    c.drawString(50, y - 40, f"Bank: Standard Bank")
    c.drawString(50, y - 60, f"Account Name: Harambee Student Living")
    c.drawString(50, y - 80, f"Account Number: 123456789")
    c.drawString(50, y - 100, f"Branch Code: 051001")
    c.drawString(50, y - 120, f"Reference: {student.name}-{room.room_number}")
    
    # Signature lines
    c.drawString(50, 120, "Student Signature: _______________________")
    c.drawString(50, 100, "Date: _______________________")
    
    c.drawString(300, 120, "Administrator Signature: _______________________")
    c.drawString(300, 100, "Date: _______________________")
    
    c.save()
    return filename

def generate_invoice(student, lease, room, payment_date=None):
    """Generate a PDF invoice"""
    filename = f"invoice_{lease.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("uploads", "invoices", filename)
    
    # Create the invoices directory if it doesn't exist
    os.makedirs(os.path.join("uploads", "invoices"), exist_ok=True)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Header - Company Info
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "INVOICE")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Invoice #: HAR-{lease.id}-{student.id:05d}")
    invoice_date = payment_date if payment_date else datetime.now()
    c.drawString(50, height - 90, f"Date: {invoice_date.strftime('%Y-%m-%d')}")
    
    # Company details on the right
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(width - 50, height - 50, "Harambee Student Living")
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 50, height - 70, "123 University Avenue")
    c.drawRightString(width - 50, height - 85, "Johannesburg, 2000")
    c.drawRightString(width - 50, height - 100, "South Africa")
    c.drawRightString(width - 50, height - 115, "admin@harambee.com")
    c.drawRightString(width - 50, height - 130, "+27 11 123 4567")
    
    # Draw a line
    c.line(50, height - 150, width - 50, height - 150)
    
    # Bill To information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 180, "Bill To:")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 200, f"{student.name}")
    c.drawString(50, height - 215, f"Room {lease.room_number}")
    c.drawString(50, height - 230, "Harambee Student Accommodation")
    
    # Lease Period
    c.setFont("Helvetica-Bold", 12)
    c.drawString(300, height - 180, "Lease Period:")
    c.setFont("Helvetica", 10)
    c.drawString(300, height - 200, f"Start Date: {lease.start_date.strftime('%Y-%m-%d')}")
    c.drawString(300, height - 215, f"End Date: {lease.end_date.strftime('%Y-%m-%d')}")
    
    # Invoice Table
    data = [
        ["Description", "Amount"],
        [f"First Month Rent - Room {lease.room_number}", f"R{room.price}"],
        ["Security Deposit (Refundable)", f"R{room.price}"],
        ["", ""],
        ["Total", f"R{room.price * 2}"]
    ]
    
    table = Table(data, colWidths=[3*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('FONT', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONT', (0, -1), (1, -1), 'Helvetica-Bold'),
        ('LINEBELOW', (0, 0), (1, 0), 1, colors.black),
        ('LINEABOVE', (0, -1), (1, -1), 1, colors.black),
        ('GRID', (0, 0), (1, -2), 0.5, colors.black),
    ]))
    
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 350)
    
    # Payment Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 400, "Payment Information:")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 420, "Payment Status: PAID")
    c.drawString(50, height - 435, f"Payment Date: {invoice_date.strftime('%Y-%m-%d')}")
    c.drawString(50, height - 450, "Payment Method: Bank Transfer")
    
    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width/2, 50, "Thank you for choosing Harambee Student Living!")
    
    c.save()
    return filename
