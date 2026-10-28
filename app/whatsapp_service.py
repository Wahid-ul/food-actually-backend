from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp_notification(booking_details):
    """
    Send WhatsApp notification to two numbers with booking details
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    
    # Two numbers to receive notifications
    to_numbers = [
        os.getenv("WHATSAPP_NOTIFICATION_NUMBER_1"),
        os.getenv("WHATSAPP_NOTIFICATION_NUMBER_2")
    ]
    
    if not all([account_sid, auth_token, from_number]):
        print("Twilio credentials not configured. Skipping WhatsApp notification.")
        return False
    
    client = Client(account_sid, auth_token)
    
    # Format the message
    message = f"""
🍽️ *New Booking Request!*

*Customer Details:*
Name: {booking_details.get('name')}
Phone: {booking_details.get('phone')}
Email: {booking_details.get('email')}

*Booking Details:*
Meal: {booking_details.get('meal_name')}
Meal Type: {booking_details.get('meal_type', 'N/A')}
Delivery Date: {booking_details.get('delivery_date')}
Delivery Slot: {booking_details.get('delivery_slot')}
Location: {booking_details.get('preferred_location')}

*Special Requests:*
{booking_details.get('special_requests', 'None')}

Please contact the customer to confirm the booking.
    """.strip()
    
    success_count = 0
    
    for to_number in to_numbers:
        if not to_number:
            continue
        
        # Skip if to_number is the same as from_number
        if to_number == from_number:
            print(f"Skipping {to_number} - cannot send to same number as Twilio WhatsApp number")
            continue
            
        try:
            # Ensure numbers are in the correct format for Twilio WhatsApp
            # Format: whatsapp:+14155238886 (for sandbox) or whatsapp:+919876543210 (for production)
            from_whatsapp = f"whatsapp:{from_number}" if not from_number.startswith("whatsapp:") else from_number
            to_whatsapp = f"whatsapp:{to_number}" if not to_number.startswith("whatsapp:") else to_number
            
            message_obj = client.messages.create(
                body=message,
                from_=from_whatsapp,
                to=to_whatsapp
            )
            print(f"WhatsApp message sent to {to_number}. SID: {message_obj.sid}")
            success_count += 1
        except Exception as e:
            print(f"Failed to send WhatsApp to {to_number}: {str(e)}")
    
    return success_count > 0
