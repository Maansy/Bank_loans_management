from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import FundRequest
# import user from django.contrib.auth.models
from django.contrib.auth.models import User
from users.models import LoanCustomer


@receiver(post_save, sender=FundRequest)
def fund_request_approved(sender, instance, created, **kwargs):
    if instance.is_approved and not created:  # Check if the fund request is approved
        # i should git the email of the user but here i will use my email
        print(f'Sending email to  abdulrahman.mostafa.mansy@gmail.com')
        email = 'abdulrahman.mostafa.mansy@gmail.com'
        send_mail(
            subject='Your fund request has been approved',
            message='Dear Customer, \n your fund request has been approved.',
            from_email='abdomansy19@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )
        print('Email sent')
