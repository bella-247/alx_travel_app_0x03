from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_booking_confirmation_email(user_email, booking_details):
    subject = "Booking Confirmation"
    message = (
        f"Dear Customer,\n\nYour booking has been confirmed!\n\n"
        f"Details:\n{booking_details}\n\nThank you for choosing ALX Travel."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
