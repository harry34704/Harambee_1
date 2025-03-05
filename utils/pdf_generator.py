
from fpdf import FPDF
import os
from datetime import datetime

def generate_lease_agreement(student, room, lease):
    """Generate a PDF lease agreement with both signatures"""
    pdf = FPDF()
    pdf.add_page()
    
    # Set styles
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(190, 10, 'HARAMBEE STUDENT LIVING', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'LEASE AGREEMENT', 0, 1, 'C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(10)
    
    # Details section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'AGREEMENT DETAILS', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    
    # Student info
    pdf.cell(50, 8, 'Student Name:', 0, 0)
    pdf.cell(140, 8, student.name, 0, 1)
    pdf.cell(50, 8, 'Student Phone:', 0, 0)
    pdf.cell(140, 8, student.phone, 0, 1)
    
    # Guardian info (if available)
    if student.guardian_name:
        pdf.cell(50, 8, 'Guardian Name:', 0, 0)
        pdf.cell(140, 8, student.guardian_name, 0, 1)
        pdf.cell(50, 8, 'Guardian Phone:', 0, 0)
        pdf.cell(140, 8, student.guardian_phone, 0, 1)
        if student.guardian_id_number:
            pdf.cell(50, 8, 'Guardian ID Number:', 0, 0)
            pdf.cell(140, 8, student.guardian_id_number, 0, 1)
        if student.guardian_street_address:
            pdf.cell(50, 8, 'Guardian Address:', 0, 0)
            pdf.cell(140, 8, student.guardian_street_address, 0, 1)
        if student.guardian_city:
            pdf.cell(50, 8, 'Guardian City:', 0, 0)
            pdf.cell(140, 8, student.guardian_city, 0, 1)
    
    # Room info
    pdf.cell(50, 8, 'Room Number:', 0, 0)
    pdf.cell(140, 8, room.room_number, 0, 1)
    pdf.cell(50, 8, 'Room Type:', 0, 0)
    pdf.cell(140, 8, room.room_type if room.room_type else 'Standard', 0, 1)
    pdf.cell(50, 8, 'Monthly Rent:', 0, 0)
    pdf.cell(140, 8, f'R{room.price}', 0, 1)
    
    # Lease period
    pdf.cell(50, 8, 'Lease Start Date:', 0, 0)
    pdf.cell(140, 8, lease.start_date.strftime('%Y-%m-%d'), 0, 1)
    pdf.cell(50, 8, 'Lease End Date:', 0, 0)
    pdf.cell(140, 8, lease.end_date.strftime('%Y-%m-%d'), 0, 1)
    
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Terms and conditions section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'TERMS AND CONDITIONS', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    
    terms = [
        "1. PREMISES: Harambee Student Living hereby agrees to rent to Student, and Student hereby agrees to rent from Harambee Student Living, the above-described premises for the stated period.",
        "2. PAYMENT: Rent is due on the 1st of each month. A late fee of R500 will be applied for payments received after the 5th of the month.",
        "3. SECURITY DEPOSIT: A security deposit equal to one month's rent is required before move-in and will be refunded within 30 days of move-out, less any deductions for damages.",
        "4. UTILITIES: Basic water and electricity are included in the rent. Excessive usage may result in additional charges.",
        "5. MAINTENANCE: Student agrees to maintain the premises in good condition and report any maintenance issues promptly through the accommodation portal.",
        "6. RULES AND REGULATIONS: Student agrees to comply with all rules and regulations as provided in the Student Handbook.",
        "7. TERMINATION: A 30-day written notice is required for termination of this agreement. Early termination may result in forfeiture of the security deposit."
    ]
    
    for term in terms:
        pdf.multi_cell(190, 8, term, 0, 'L')
        pdf.ln(5)
    
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    # Signatures section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'SIGNATURES', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    
    # Student signature
    pdf.cell(50, 8, 'Student Signature:', 0, 0)
    pdf.cell(140, 8, lease.student_signature, 0, 1)
    pdf.cell(50, 8, 'Date Signed:', 0, 0)
    pdf.cell(140, 8, lease.student_signature_date.strftime('%Y-%m-%d %H:%M'), 0, 1)
    
    # Guardian signature (if available)
    if lease.guardian_signature:
        pdf.cell(50, 8, 'Guardian Signature:', 0, 0)
        pdf.cell(140, 8, lease.guardian_signature, 0, 1)
    
    # Admin signature
    if lease.admin_signature:
        pdf.cell(50, 8, 'Administrator Signature:', 0, 0)
        pdf.cell(140, 8, lease.admin_signature, 0, 1)
        pdf.cell(50, 8, 'Date Signed:', 0, 0)
        pdf.cell(140, 8, lease.admin_signature_date.strftime('%Y-%m-%d %H:%M'), 0, 1)
    
    # IP address and timestamp
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(190, 8, f'This agreement was electronically signed from IP: {lease.signature_ip}', 0, 1)
    pdf.cell(190, 8, f'Document generated on: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}', 0, 1)
    pdf.cell(190, 8, f'Agreement ID: {lease.id}', 0, 1)
    
    # Save the PDF
    upload_folder = "uploads"
    lease_dir = os.path.join(upload_folder, "leases")
    os.makedirs(lease_dir, exist_ok=True)
    
    filename = f"lease_agreement_{lease.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    file_path = os.path.join(lease_dir, filename)
    
    pdf.output(file_path)
    return filename

def generate_invoice(student, room, lease):
    """Generate an invoice PDF for the lease"""
    pdf = FPDF()
    pdf.add_page()
    
    # Set styles
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(190, 10, 'HARAMBEE STUDENT LIVING', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'OFFICIAL INVOICE', 0, 1, 'C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(10)
    
    # Invoice details
    now = datetime.now()
    invoice_number = f"INV-{lease.id}-{lease.created_at.strftime('%Y%m%d')}"
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(95, 10, 'INVOICE TO:', 0, 0)
    pdf.cell(95, 10, 'INVOICE DETAILS:', 0, 1)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(95, 8, student.name, 0, 0)
    pdf.cell(40, 8, 'Invoice Number:', 0, 0)
    pdf.cell(55, 8, invoice_number, 0, 1)
    
    pdf.cell(95, 8, f'Room {lease.room_number}', 0, 0)
    pdf.cell(40, 8, 'Date:', 0, 0)
    pdf.cell(55, 8, now.strftime('%Y-%m-%d'), 0, 1)
    
    pdf.cell(95, 8, student.phone, 0, 0)
    pdf.cell(40, 8, 'Status:', 0, 0)
    pdf.cell(55, 8, 'PAID', 0, 1)
    
    pdf.ln(10)
    
    # Invoice items table header
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(120, 10, 'Description', 1, 0, 'L', 1)
    pdf.cell(70, 10, 'Amount', 1, 1, 'R', 1)
    
    # Invoice items
    pdf.set_font('Arial', '', 10)
    pdf.cell(120, 10, f'Accommodation Fee - Room {lease.room_number} (First Month)', 1, 0, 'L')
    pdf.cell(70, 10, f'R{room.price}', 1, 1, 'R')
    
    pdf.cell(120, 10, 'Security Deposit', 1, 0, 'L')
    pdf.cell(70, 10, f'R{room.price}', 1, 1, 'R')
    
    # Total
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(120, 10, 'Total', 1, 0, 'L', 1)
    pdf.cell(70, 10, f'R{float(room.price) * 2}', 1, 1, 'R', 1)
    
    pdf.ln(10)
    
    # Payment information
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'PAYMENT INFORMATION', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.cell(190, 8, 'Bank Transfer to Standard Bank', 0, 1)
    pdf.cell(190, 8, 'Account: 123456789', 0, 1)
    pdf.cell(190, 8, f'Reference: STU{student.id}', 0, 1)
    
    pdf.ln(10)
    
    # Terms and notes
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'TERMS & CONDITIONS', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(190, 8, 'This invoice confirms your payment has been received and your accommodation has been secured for the specified period. Please refer to your signed lease agreement for all terms and conditions regarding your stay.', 0, 'L')
    
    # Save the PDF
    upload_folder = "uploads"
    invoice_dir = os.path.join(upload_folder, "invoices")
    os.makedirs(invoice_dir, exist_ok=True)
    
    filename = f"invoice_{lease.id}_{now.strftime('%Y%m%d%H%M%S')}.pdf"
    file_path = os.path.join(invoice_dir, filename)
    
    pdf.output(file_path)
    return filename
