from django.contrib import admin
from .models import Merchant, User, Customer

# Register your models here.

admin.site.register(Merchant)
admin.site.register(Customer)


class UserAdmin(admin.ModelAdmin):

    prepopulated_fields = {
        "slug": [
            "first_name",
            "last_name",
        ],
    }


admin.site.register(User, UserAdmin)
