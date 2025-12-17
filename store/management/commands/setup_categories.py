from django.core.management.base import BaseCommand

from store.models import Category


class Command(BaseCommand):
    help = "Creates initial category structure for the e-commerce platform"

    def handle(self, *args, **options):
        self.stdout.write("Creating Categories...")
        Category.objects.all().delete()
        categories_structure = {
            "Electronics": {
                "icon": "fa-laptop",
                "subcategories": {
                    "Phones": "phone",
                    "Laptops": "laptop",
                    "Tablets": "tablet",
                    "Headphones": "headphone",
                },
            },
            "Fashion": {
                "icon": "fa-shirt",
                "subcategories": {
                    "Clothing": "clothing",
                    "Shoes": "shoe",
                    "Watches": "watch",
                },
            },
            "Sports": {
                "icon": "fa-football",
                "subcategories": {
                    "Sport Equipment": "sport_equipment",
                },
            },
        }

        for key, value in categories_structure.items():
            main_category = Category.objects.create(
                name=key,
            )
            self.stdout.write(f"created main category '{main_category}' ")
            for sub_category, model_name in value["subcategories"].items():
                Category.objects.create(
                    name=sub_category, parent=main_category, model_name=model_name
                )
                self.stdout.write(f"created sub-category '{sub_category}' ")

        self.stdout.write(self.style.SUCCESS("\nAll categories created successfully!"))
