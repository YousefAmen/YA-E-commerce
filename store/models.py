import datetime
import uuid
from django.db import models
from members.models import Merchant
from django.core.validators import MinLengthValidator
from django.template.defaultfilters import slugify

from cloudinary.models import CloudinaryField
from ecom import settings
from django.db.models import Count, Sum


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    name = models.CharField(
        max_length=500,
        default=None,
        verbose_name="Category Name",
        validators=[
            MinLengthValidator(3, "the field must contain at least 20 character")
        ],
    )
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def category_product_count(self):
        return self.products.count()

    @property
    def total_sales(self):
        return self.products.aggregate(top=Count("product"))["top"]

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(
        Merchant, on_delete=models.CASCADE, related_name="products"
    )
    product_model = models.CharField(
        max_length=1000,
        default=None,
        validators=[
            MinLengthValidator(3, "the field must contain at least 3 character")
        ],
        null=True,
        blank=True,
        verbose_name="Product Brand",
    )
    name = models.CharField(
        max_length=1500,
        default=None,
        verbose_name="Product Name",
        validators=[
            MinLengthValidator(2, "the field must contain at least 2 character")
        ],
    )

    description = models.TextField(
        max_length=1500,
        default=None,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(10, "the field must contain at least 10 characters")
        ],
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, verbose_name="Product Price"
    )
    discount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
        verbose_name="Dicount",
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=1, related_name="products"
    )
    favourites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
    )
    views_number = models.PositiveIntegerField(default=0)

    views = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="user_views", blank=True
    )
    visitors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="product_visitors", blank=True
    )
    slug = models.SlugField(null=True, blank=True, max_length=1500)
    added = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    @property
    def final_price(self):
        if self.discount and self.discount < self.price:
            return max(self.price - self.discount, 2)

    @property
    def discount_percentage(self):
        if self.price and self.discount:
            return round(self.discount / self.price * 100, 2)
        return 0

    @property
    def sold_count(self):
        return self.product.count()

    def __str__(self):
        return self.name


class Attribute(models.Model):
    ATTRIBUTE_TYPES = (
        ("text", "Text"),
        ("number", "Number"),
        ("boolean", "Yes/No"),
        ("choice", "Dropdown"),
    )

    name = models.CharField(max_length=100)
    attribute_type = models.CharField(max_length=20, choices=ATTRIBUTE_TYPES)
    unit = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} ({self.unit})" if self.unit else self.name


class CategoryAttribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=False)

    class Meta:
        unique_together = ("category", "attribute")

    def __str__(self):
        return f"{self.category.name} - {self.attribute.name}"


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_attribute"
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=500)

    class Meta:
        unique_together = ("product", "attribute")

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"


class ProductImage(models.Model):
    image = CloudinaryField("image", resource_type="image")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image {self.id}"


class Inventory(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="inventory"
    )
    quantity = models.PositiveIntegerField()
    last_restocked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - Stock: {self.quantity}"


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=250)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.email}"


class SiteStats(models.Model):
    auth_visitors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="site_visists", blank=True
    )
    anonymous_visitor_count = models.IntegerField(default=0)

    def total_visitores(self):
        return self.auth_visitors.count() + self.anonymous_visitor_count
