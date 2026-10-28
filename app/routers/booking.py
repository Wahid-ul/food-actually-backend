from fastapi import APIRouter
from ..schemas import BookingCreate
from ..whatsapp_service import send_whatsapp_notification

router = APIRouter(prefix="/booking", tags=["Booking"])


@router.post("/submit")
def submit_booking(booking: BookingCreate):
    """
    Submit a booking request and send WhatsApp notification
    """
    booking_details = {
        "name": booking.name,
        "phone": booking.phone,
        "email": booking.email,
        "meal_name": booking.meal_name,
        "meal_type": booking.meal_type,
        "delivery_date": booking.delivery_date,
        "delivery_slot": booking.delivery_slot,
        "preferred_location": booking.preferred_location,
        "special_requests": booking.special_requests,
    }
    
    # Send WhatsApp notification
    notification_sent = send_whatsapp_notification(booking_details)
    
    return {
        "message": "Booking submitted successfully",
        "notification_sent": notification_sent
    }
