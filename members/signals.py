from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, Merchant, Customer
from django.dispatch import Signal, receiver

user_signed_up = Signal()


@receiver(user_signed_up)
def create_user_profile(sender, user, signup_data, **kwargs):
    if signup_data:
        if signup_data["role"] == "merchant":
            Merchant.objects.create(user=user)
        else:
            Customer.objects.create(user=user)
