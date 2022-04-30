from django.core.mail import EmailMessage
from django.conf import settings


def mail(message,recipient_list):
    settings.configure()
    email = EmailMessage(
    'From PITBULL',
    message,
    settings.EMAIL_HOST_USER,
    recipient_list,
    )
    
    email.send()
    return email

mail('DHHDHDHD',['mahimanu66@gmail.com'])