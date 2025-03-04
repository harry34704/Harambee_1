
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import Table, TableStyle
from datetime import datetime

def generate_lease_agreement(student, room, start_date, end_date):
    """Generate a PDF lease agreement"""
    # Create the directory if it doesn't exist
    lease_dir = os.path.join("uploads", "leases")
    os.makedirs(lease_dir, exist_ok=True)
    
    # Generate unique filename
    filename = f"lease_{student.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join(lease_dir, filename)
    
    # Create PDF
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    
    # Logo and Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(1*inch, 10*inch, "HARAMBEE ACCOMMODATION")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, 9.5*inch, "LEASE AGREEMENT")
    
    # Add line under the header
    c.setStrokeColor(colors.black)
    c.line(1*inch, 9.3*inch, 7.5*inch, 9.3*inch)
    
    # Lease information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, 8.7*inch, "STUDENT INFORMATION")
    
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 8.4*inch, f"Name: {student.name}")
    c.drawString(1*inch, 8.2*inch, f"Email: {student.user.email}")
    c.drawString(1*inch, 8.0*inch, f"Phone: {student.phone}")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, 7.5*inch, "ACCOMMODATION DETAILS")
    
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 7.2*inch, f"Room Number: {room.room_number}")
    c.drawString(1*inch, 7.0*inch, f"Room Type: {room.room_type}")
    c.drawString(1*inch, 6.8*inch, f"Rental Amount: R{room.price} per month")
    c.drawString(1*inch, 6.6*inch, f"Lease Start Date: {start_date.strftime('%d %B %Y')}")
    c.drawString(1*inch, 6.4*inch, f"Lease End Date: {end_date.strftime('%d %B %Y')}")
    
    # Terms and conditions
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, 6.0*inch, "TERMS AND CONDITIONS")
    
    terms = [
        "1. The Tenant agrees to pay the full rental amount by bank transfer.",
        "2. The Tenant shall maintain the premises in good condition.",
        "3. The Tenant shall not sublet the premises without written consent.",
        "4. The Tenant agrees to comply with residence rules and regulations.",
        "5. A security deposit of R1000 is required, refundable upon inspection.",
        "6. The Tenant must provide 30 days notice before termination.",
        "7. Damages beyond normal wear and tear are the Tenant's responsibility.",
        "8. Utilities are included in the rental amount.",
        "9. The Landlord may enter the premises for maintenance with notice.",
        "10. Violation of these terms may result in termination of the lease."
    ]
    
    y_position = 5.8*inch
    c.setFont("Helvetica", 9)
    for term in terms:
        c.drawString(1*inch, y_position, term)
        y_position -= 0.2*inch
    
    # Bank Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, 3.3*inch, "PAYMENT DETAILS")
    
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 3.0*inch, "Bank Name: First National Bank")
    c.drawString(1*inch, 2.8*inch, "Account Holder: Harambee Accommodation")
    c.drawString(1*inch, 2.6*inch, "Account Number: 62123456789")
    c.drawString(1*inch, 2.4*inch, "Branch Code: 250655")
    c.drawString(1*inch, 2.2*inch, f"Reference: HAR{student.id}-{room.room_number}")
    
    # Signature
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, 1.8*inch, "AGREEMENT CONFIRMATION")
    
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 1.5*inch, f"Student Name: {student.name}")
    c.drawString(1*inch, 1.3*inch, f"Signed digitally on: {datetime.now().strftime('%d %B %Y')}")
    
    # Add a line for official use
    c.line(1*inch, 0.8*inch, 3*inch, 0.8*inch)
    c.drawString(1.5*inch, 0.6*inch, "Student Signature")
    
    c.line(5*inch, 0.8*inch, 7*inch, 0.8*inch)
    c.drawString(5.5*inch, 0.6*inch, "Landlord Signature")
    
    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(2.5*inch, 0.3*inch, "Harambee Accommodation - Student Housing")
    
    c.save()
    return filename

def generate_invoice(student, lease, room):
    """Generate a PDF invoice"""
    # Create the directory if it doesn't exist
    invoice_dir = os.path.join("uploads", "invoices")
    os.makedirs(invoice_dir, exist_ok=True)
    
    # Generate unique filename
    invoice_number = f"INV-{lease.id}-{datetime.now().strftime('%Y%m%d')}"
    filename = f"invoice_{student.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join(invoice_dir, filename)
    
    # Create PDF
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    
    # Logo and Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(1*inch, 10*inch, "HARAMBEE ACCOMMODATION")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, 9.7*inch, "123 Student Street, City, 2001")
    c.drawString(1*inch, 9.5*inch, "Email: info@harambee.com")
    
    # Invoice Title and Number
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, 8.8*inch, "INVOICE")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 8.5*inch, f"Invoice Number: {invoice_number}")
    c.drawString(1*inch, 8.3*inch, f"Date: {datetime.now().strftime('%d %B %Y')}")
    
    # Billed To
    c.setFont("Helvetica-Bold", 12)
    c.drawString(5*inch, 8.8*inch, "BILLED TO:")
    c.setFont("Helvetica", 10)
    c.drawString(5*inch, 8.5*inch, student.name)
    c.drawString(5*inch, 8.3*inch, f"Phone: {student.phone}")
    c.drawString(5*inch, 8.1*inch, f"Email: {student.user.email}")
    
    # Add line under the header
    c.setStrokeColor(colors.black)
    c.line(1*inch, 7.8*inch, 7.5*inch, 7.8*inch)
    
    # Invoice details table
    data = [
        ['Description', 'Period', 'Amount'],
        [f'Room {room.room_number} ({room.room_type})',
         f'{lease.start_date.strftime("%d %b %Y")} - {lease.end_date.strftime("%d %b %Y")}',
         f'R {room.price}'],
        ['', 'Total:', f'R {room.price}']
    ]
    
    table = Table(data, colWidths=[3*inch, 2*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
        ('GRID', (0, 0), (-1, -2), 0.5, colors.black),
    ]))
    
    table.wrapOn(c, width, height)
    table.drawOn(c, 1*inch, 7*inch)
    
    # Payment Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, 6*inch, "PAYMENT INFORMATION")
    
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 5.7*inch, "Payment received via bank transfer")
    c.drawString(1*inch, 5.5*inch, f"Reference: HAR{student.id}-{room.room_number}")
    
    # Payment Status
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.green)
    c.drawString(6*inch, 5.7*inch, "PAID")
    c.setFillColor(colors.black)
    
    # Terms and Notes
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, 4.8*inch, "NOTES")
    
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, 4.5*inch, "Thank you for choosing Harambee Accommodation.")
    c.drawString(1*inch, 4.3*inch, "This invoice serves as proof of payment for your accommodation.")
    
    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(2.5*inch, 0.3*inch, "Harambee Accommodation - Student Housing")
    
    c.save()
    return filename
