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
    model_name = models.CharField(max_length=50, null=True, blank=True)
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

    @property
    def views_count(self):
        return self.views.count()

    def __str__(self):
        return self.name


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


class Phone(Product):
    screen_size = models.FloatField(help_text="In inches")
    screen_type = models.CharField(
        max_length=50,
        choices=[
            ("AMOLED", "AMOLED"),
            ("LCD", "LCD"),
            ("OLED", "OLED"),
            ("IPS", "IPS"),
        ],
    )
    processor = models.CharField(max_length=100)
    ram = models.IntegerField(help_text="In GB")
    storage = models.IntegerField(help_text="In GB")
    battery_capacity = models.IntegerField(help_text="In mAh")
    rear_camera = models.CharField(max_length=100, help_text="e.g., 48MP + 12MP")
    front_camera = models.CharField(max_length=50, help_text="e.g., 12MP")
    operating_system = models.CharField(
        max_length=50,
        choices=[("Android", "Android"), ("iOS", "iOS"), ("Other", "Other")],
    )
    network = models.CharField(max_length=20, choices=[("4G", "4G"), ("5G", "5G")])
    color = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Phones"


class Laptop(Product):
    screen_size = models.FloatField(help_text="In inches")
    processor = models.CharField(max_length=100, help_text="e.g., Intel Core i7")
    processor_generation = models.CharField(max_length=50)
    ram = models.IntegerField(help_text="In GB")
    storage_type = models.CharField(
        max_length=20, choices=[("SSD", "SSD"), ("HDD", "HDD"), ("Hybrid", "Hybrid")]
    )
    storage_capacity = models.IntegerField(help_text="In GB")
    graphics_card = models.CharField(max_length=100)
    operating_system = models.CharField(
        max_length=50,
        choices=[
            ("Windows 11", "Windows 11"),
            ("Windows 10", "Windows 10"),
            ("macOS", "macOS"),
            ("Linux", "Linux"),
        ],
    )
    battery_life = models.IntegerField(help_text="In hours")
    weight = models.FloatField(help_text="In kg")
    color = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Laptops"


class Tablet(Product):
    screen_size = models.FloatField(help_text="In inches")
    processor = models.CharField(max_length=100)
    ram = models.IntegerField(help_text="In GB")
    storage = models.IntegerField(help_text="In GB")
    battery_capacity = models.IntegerField(help_text="In mAh")
    camera = models.CharField(max_length=50)
    operating_system = models.CharField(
        max_length=50,
        choices=[("Android", "Android"), ("iOS", "iOS"), ("Windows", "Windows")],
    )
    has_sim_card = models.BooleanField(default=False)
    color = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Tablets"


class Headphone(Product):
    """Headphones and Earphones"""

    headphone_type = models.CharField(
        max_length=50,
        choices=[
            ("Over-Ear", "Over-Ear"),
            ("On-Ear", "On-Ear"),
            ("In-Ear", "In-Ear"),
            ("Earbuds", "Earbuds"),
        ],
    )
    connection_type = models.CharField(
        max_length=20, choices=[("Wireless", "Wireless"), ("Wired", "Wired")]
    )
    noise_cancellation = models.BooleanField(default=False)
    battery_life = models.IntegerField(help_text="In hours", null=True, blank=True)
    driver_size = models.IntegerField(help_text="In mm", null=True, blank=True)
    color = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Headphones"


class Clothing(Product):
    clothing_type = models.CharField(
        max_length=50,
        choices=[
            ("T-Shirt", "T-Shirt"),
            ("Shirt", "Shirt"),
            ("Pants", "Pants"),
            ("Jeans", "Jeans"),
            ("Dress", "Dress"),
            ("Jacket", "Jacket"),
            ("Sweater", "Sweater"),
        ],
    )
    gender = models.CharField(
        max_length=20,
        choices=[("Men", "Men"), ("Women", "Women"), ("Unisex", "Unisex")],
    )
    size = models.CharField(
        max_length=10,
        choices=[
            ("XS", "XS"),
            ("S", "S"),
            ("M", "M"),
            ("L", "L"),
            ("XL", "XL"),
            ("XXL", "XXL"),
        ],
    )
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100, help_text="e.g., Cotton, Polyester")
    season = models.CharField(
        max_length=20,
        choices=[
            ("Summer", "Summer"),
            ("Winter", "Winter"),
            ("All Season", "All Season"),
        ],
    )

    class Meta:
        verbose_name_plural = "Clothing"


class Shoe(Product):
    shoe_type = models.CharField(
        max_length=50,
        choices=[
            ("Sneakers", "Sneakers"),
            ("Boots", "Boots"),
            ("Sandals", "Sandals"),
            ("Formal", "Formal"),
            ("Sports", "Sports"),
        ],
    )
    gender = models.CharField(
        max_length=20,
        choices=[("Men", "Men"), ("Women", "Women"), ("Unisex", "Unisex")],
    )
    size = models.IntegerField(help_text="US size")
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100, help_text="e.g., Leather, Canvas")

    class Meta:
        verbose_name_plural = "Shoes"


class Watch(Product):
    watch_type = models.CharField(
        max_length=50,
        choices=[
            ("Analog", "Analog"),
            ("Digital", "Digital"),
            ("Smart Watch", "Smart Watch"),
        ],
    )
    gender = models.CharField(
        max_length=20,
        choices=[("Men", "Men"), ("Women", "Women"), ("Unisex", "Unisex")],
    )
    strap_material = models.CharField(
        max_length=50,
        choices=[
            ("Leather", "Leather"),
            ("Metal", "Metal"),
            ("Rubber", "Rubber"),
            ("Fabric", "Fabric"),
        ],
    )
    water_resistant = models.BooleanField(default=False)
    display_type = models.CharField(max_length=50, null=True, blank=True)
    battery_type = models.CharField(
        max_length=50,
        choices=[
            ("Quartz", "Quartz"),
            ("Automatic", "Automatic"),
            ("Rechargeable", "Rechargeable"),
        ],
    )
    color = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Watches"


class SportEquipment(Product):
    """Sports Equipment"""

    sport_type = models.CharField(
        max_length=50,
        choices=[
            ("Football", "Football"),
            ("Basketball", "Basketball"),
            ("Tennis", "Tennis"),
            ("Gym", "Gym"),
            ("Cycling", "Cycling"),
            ("Swimming", "Swimming"),
        ],
    )
    equipment_type = models.CharField(
        max_length=100, help_text="e.g., Ball, Racket, Dumbbell"
    )
    material = models.CharField(max_length=100)
    size = models.CharField(max_length=50, null=True, blank=True)
    weight = models.FloatField(help_text="In kg", null=True, blank=True)
    color = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Sport Equipment"


class Book(Product):
    author = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=13, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Books"


class Review(models.Model):
    RATING_CHOICES = (
        (1, "1 - Poor"),
        (2, "2 - Fair"),
        (3, "3 - Good"),
        (4, "4 - Vary Good"),
        (5, "5 - Excellent"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_reviews"
    )

    rate = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, null=True, blank=True
    )
    body = models.TextField(max_length=300)
    slug = models.SlugField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["product", "user"]

    def save(self, *args, **kwargs):

        self.slug = slugify(self.body[:50])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reviewing by {self.user.first_name} {self.user.last_name} for {self.course}"


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
