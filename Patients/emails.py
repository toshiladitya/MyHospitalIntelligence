from django.core.mail import send_mail
import random
from django.conf import settings
from Patients.models import Patient
def send_otp_via_mail(email):
    subject='Your account verification email'
    otp=random.randint(1000,9999)
    message=f'To verify your {email} please enter your otp {otp}'
    email_from=settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,[email])
    patient_object=Patient.objects.get(email=email)
    patient_object.otp=otp
    patient_object.save()
    
    
def password_reset_mail(email):
    subject='Your account verification email'
    otp=random.randint(1000,9999)
    message=f'To reset your password for email {email} please enter your otp {otp}'
    email_from=settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,[email])
    patient_object=Patient.objects.get(email=email)
    patient_object.otp=otp
    patient_object.save()
    
    
    
