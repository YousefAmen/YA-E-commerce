from django.contrib import admin
from . import models
from members.models import User


admin.site.site_header = "Y-A-A"


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Category)
admin.site.register(models.Contact)
admin.site.register(models.Product)
admin.site.register(models.Inventory)
admin.site.register(models.ProductImage)
admin.site.register(models.Laptop)
admin.site.register(models.Phone)
admin.site.register(models.Book)
