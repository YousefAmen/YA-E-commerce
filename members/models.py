from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField
from .managers import UserManager
import uuid
from django.shortcuts import reverse
from slugify import slugify
from ecom import settings


class User(AbstractUser):
    class Role(models.TextChoices):
        MERCHANT = "merchant", "Merchant"
        CUSTOMER = "customer", "Customer"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=255, choices=Role.choices, default=Role.CUSTOMER)
    bio = models.TextField(max_length=500, blank=True, null=True)
    gender = models.CharField(
        max_length=255, choices=Gender.choices, default=Gender.MALE
    )
    profile_image = CloudinaryField("image", null=True, blank=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = CountryField()
    joined_at = models.DateTimeField(default=datetime.now)
    slug = models.SlugField(default="")
    objects = UserManager()
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.first_name}-{self.last_name}")
        if not self.id:
            self.id = uuid.uuid4().hex[:16].upper()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("members:user_profile", args=[self.slug, self.id])


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer_profile"
    )
    shipping_address = models.TextField(blank=True)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return f"Customer: {self.user.email}"


class Merchant(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="marchant_profile"
    )
    business_name = models.CharField(max_length=255)
    store_description = models.TextField(max_length=700)
    business_phone = models.CharField(max_length=11)
    business_address = models.TextField()
    visitors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="visited_merchants", blank=True
    )

    def __str__(self):
        if self.business_name:
            return self.business_name
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def visitor_count(self):
        return self.visitors.count()
