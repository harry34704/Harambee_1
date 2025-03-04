import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from twilio.rest import Client
from datetime import datetime

def generate_lease_pdf(student, room, start_date, end_date):
    """Generate a PDF lease agreement"""
    filename = f"lease_{student.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("uploads", filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    c.drawString(100, 750, "HARAMBEE ACCOMMODATION LEASE AGREEMENT")
    c.drawString(100, 700, f"Student Name: {student.name}")
    c.drawString(100, 675, f"Room Number: {room.room_number}")
    c.drawString(100, 650, f"Start Date: {start_date}")
    c.drawString(100, 625, f"End Date: {end_date}")
    c.save()
    
    return filename

def send_sms_notification(phone_number, message):
    """Send SMS using Twilio"""
    client = Client(
        os.environ.get("TWILIO_ACCOUNT_SID"),
        os.environ.get("TWILIO_AUTH_TOKEN")
    )
    
    try:
        message = client.messages.create(
            body=message,
            from_=os.environ.get("TWILIO_PHONE_NUMBER"),
            to=phone_number
        )
        return True
    except Exception as e:
        print(f"SMS sending failed: {str(e)}")
        return False

def allowed_file(filename):
    """Check if uploaded file type is allowed"""
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
