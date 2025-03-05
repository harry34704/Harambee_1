import os
from twilio.rest import Client

def send_sms_notification(phone_number, message):
    """Send SMS using Twilio"""
    try:
        # Check if Twilio credentials are configured
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        from_number = os.environ.get("TWILIO_PHONE_NUMBER")

        if not (account_sid and auth_token and from_number):
            print("Twilio credentials not configured. SMS not sent.")
            return False

        client = Client(account_sid, auth_token)

        # Clean up the phone number if needed
        # Make sure it has international format (e.g., +27)
        if not phone_number.startswith('+'):
            # Assuming South African numbers, add +27 prefix
            if phone_number.startswith('0'):
                phone_number = '+27' + phone_number[1:]
            else:
                phone_number = '+27' + phone_number

        message = client.messages.create(
            body=message,
            from_=from_number,
            to=phone_number
        )
        print(f"SMS sent to {phone_number}: {message.sid}")
        return True
    except Exception as e:
        print(f"SMS sending failed: {str(e)}")
        return False

def send_application_status(student, status):
    """Send application status notification to student"""
    message = f"Hello {student.name}, "

    if status == "approve":
        message += "Your application for Harambee Accommodation has been APPROVED! You can log in to your account to view your lease agreement and invoice."
    elif status == "partial_approve":
        message += "Your application has been PARTIALLY APPROVED. Please log in to your account to sign your lease agreement."
    elif status == "reject":
        message += "Unfortunately, your application for Harambee Accommodation has been REJECTED. Please contact our office for more information."
    elif status == "hold":
        message += "Your application for Harambee Accommodation is ON HOLD. Please log in to your account to see what additional documents or information are needed."
    else:
        message += f"Your application status has been updated to: {status.upper()}"

    return send_sms_notification(student.phone, message)

def send_lease_notification(student, lease, action):
    """Send lease-related notifications"""
    message = f"Hello {student.name}, "

    if action == "generated":
        message += "Your lease agreement for Harambee Accommodation has been generated and is ready for your signature. Please log in to your account to review and sign it."
    elif action == "admin_signed":
        message += "Your lease agreement has been signed by the administrator. You can now proceed with payment."
    elif action == "payment_verified":
        message += "Your payment has been verified! Your room is now confirmed. You can download your invoice from your dashboard."
    elif action == "payment_rejected":
        message += "Your payment proof has been rejected. Please upload a valid payment proof."

    return send_sms_notification(student.phone, message)