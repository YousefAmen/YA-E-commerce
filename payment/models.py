from django.db import models
from django.core.validators import MinLengthValidator
from store.models import Product
import uuid
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime
from django_countries.fields import CountryField
from ecom import settings
from members.models import Merchant, Customer


class ShippingAddress(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    shipping_full_name = models.CharField(
        max_length=255,
    )
    shipping_email = models.EmailField(max_length=50, null=True, blank=True)
    shipping_address1 = models.CharField(max_length=400, verbose_name="Address")
    shipping_address2 = models.CharField(max_length=400, verbose_name="Address")
    building_name = models.CharField(
        max_length=400, verbose_name="Building Name", null=True
    )
    shipping_phone = models.CharField(
        max_length=17,
        validators=[MinLengthValidator(11, "The Field Must be contain 11 Numbers")],
    )
    shipping_city = models.CharField(max_length=255, blank=True)
    shipping_state = models.CharField(max_length=255, blank=True)
    shipping_zipcode = models.CharField(max_length=255, blank=True)
    shipping_country = CountryField()

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return (
            f"{self.shipping_full_name} - {self.shipping_city}, {self.shipping_country}"
        )

    @property
    def get_full_address(self):
        return f"""{self.shipping_full_name}
        {self.shipping_address1}
        {self.shipping_address2}
        {self.building_name if self.building_name else ''}
        {self.shipping_city}, {self.shipping_state} {self.shipping_zipcode}
        {self.shipping_country}
        Phone: {self.shipping_phone}"""


class Order(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        PENDING = (
            "pending",
            "Pending",
        )
        CONFIRMED = (
            "confirmed",
            "Confirmed",
        )
        DELIVERED = (
            "delivered",
            "Delivered",
        )
        SHIPPED = (
            "shipped",
            "Shipped",
        )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.PENDING
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="orders",
    )
    merchant = models.ForeignKey(
        Merchant, on_delete=models.CASCADE, related_name="orders", null=True, blank=True
    )
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.CASCADE, related_name="shipping_address"
    )
    summary_shipping_address = models.TextField(max_length=15000, default=None)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date_shipped = models.DateTimeField(blank=True, null=True)
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{str(self.id)[:8]} - {self.email}"


# add the date time when the product marked as shipped
@receiver(pre_save, sender=Order)
def set_shipped_date(sender, instance, **kwargs):
    if instance.pk and instance.status == "shipped":
        instance.date_shipped = datetime.datetime.now()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, related_name="order_items"
    )
    products = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user"
    )
    quantity = models.PositiveIntegerField(null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'Product : {self.products.name if self.products else "No Product"}'
