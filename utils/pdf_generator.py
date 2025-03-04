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
