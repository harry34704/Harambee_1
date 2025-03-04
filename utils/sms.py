import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

def send_sms_notification(to_number, message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return True
    except Exception as e:
        print(f"SMS sending failed: {str(e)}")
        return False

def send_application_status(student, status):
    message = f"Dear {student.name}, your Harambee accommodation application has been {status}."
    if status == "approved":
        message += " Please log in to complete your lease agreement."
    return send_sms_notification(student.phone, message)

def send_maintenance_update(student, request_id, status):
    message = f"Dear {student.name}, your maintenance request #{request_id} status has been updated to: {status}"
    return send_sms_notification(student.phone, message)
