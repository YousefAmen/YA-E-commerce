from django.core.management.base import BaseCommand

from store.models import Category, Attribute, CategoryAttribute


class Command(BaseCommand):
    help = "Creates initial category structure for the e-commerce platform"

    def handle(self, *args, **options):
        self.stdout.write("Creating Categories...")
        Category.objects.all().delete()
        Attribute.objects.all().delete()
        CategoryAttribute.objects.all().delete()
        categories_structure = {
            "Electronics": ["Phones", "Laptops", "Tablets", "Headphones"],
            "Fashion": ["Clothing", "Shoes", "Watches"],
            "Sports": ["Sport Equipment"],
        }
        created_categories = {}
        for main_category_name, subcategories in categories_structure.items():
            main_category = Category.objects.create(name=main_category_name)
            created_categories[main_category_name] = main_category
            self.stdout.write(f"Created main category:{main_category_name}")
            for sub_category_name in subcategories:
                sub_category = Category.objects.create(
                    name=sub_category_name, parent=main_category
                )
                created_categories[sub_category_name] = sub_category
                self.stdout.write(f"Created Subcategory {sub_category_name}")
        self.stdout.write(self.style.SUCCESS("All categories created !"))

        self.stdout.write(self.style.SUCCESS("Creating Attributes..."))

        attributes_data = {
            "Camera": {"type": "number", "unit": "MP"},
            "Battery": {"type": "number", "unit": "mAh"},
            "Storage": {"type": "number", "unit": "GB"},
            "RAM": {"type": "number", "unit": "GB"},
            "Screen Size": {"type": "number", "unit": "inch"},
            "Operating System": {"type": "text", "unit": ""},
            "5G Support": {"type": "boolean", "unit": ""},
            "Processor": {"type": "text", "unit": ""},
            "Graphics Card": {"type": "text", "unit": ""},
            "SSD": {"type": "number", "unit": "GB"},
            "Weight": {"type": "number", "unit": "kg"},
            "Stylus Support": {"type": "boolean", "unit": ""},
            "Keyboard Included": {"type": "boolean", "unit": ""},
            "Wireless": {"type": "boolean", "unit": ""},
            "Noise Cancellation": {"type": "boolean", "unit": ""},
            "Battery Life": {"type": "number", "unit": "hours"},
            "Driver Size": {"type": "number", "unit": "mm"},
            "Size": {"type": "text", "unit": ""},
            "Color": {"type": "text", "unit": ""},
            "Material": {"type": "text", "unit": ""},
            "Gender": {"type": "text", "unit": ""},
            "Shoe Size": {"type": "text", "unit": ""},
            "Shoe Type": {"type": "text", "unit": ""},
            "Watch Type": {"type": "text", "unit": ""},
            "Water Resistant": {"type": "boolean", "unit": ""},
            "Strap Material": {"type": "text", "unit": ""},
            "Sport Type": {"type": "text", "unit": ""},
            "Suitable For": {"type": "text", "unit": ""},
        }
        created_attributes = {}
        for attr_name, attr_config in attributes_data.items():
            attribute = Attribute.objects.create(
                name=attr_name,
                attribute_type=attr_config["type"],
                unit=attr_config["unit"],
            )
            created_attributes[attr_name] = attribute
            unit = f"{attr_config['unit']}" if attr_config["unit"] else ""
            self.stdout.write(
                f"Created attribute: {attr_name}{unit} [{attr_config['type']}]"
            )
        self.stdout.write(self.style.SUCCESS("All attributes created!"))

        category_attribute_mapping = {
            "Phones": [
                {"attr": "Camera", "required": True},
                {"attr": "Battery", "required": True},
                {"attr": "Storage", "required": True},
                {"attr": "RAM", "required": True},
                {"attr": "Screen Size", "required": True},
                {"attr": "Operating System", "required": True},
                {"attr": "5G Support", "required": False},
            ],
            "Laptops": [
                {"attr": "Processor", "required": True},
                {"attr": "RAM", "required": True},
                {"attr": "Storage", "required": True},
                {"attr": "SSD", "required": False},
                {"attr": "Graphics Card", "required": False},
                {"attr": "Screen Size", "required": True},
                {"attr": "Weight", "required": False},
                {"attr": "Operating System", "required": True},
            ],
            "Tablets": [
                {"attr": "Screen Size", "required": True},
                {"attr": "Storage", "required": True},
                {"attr": "RAM", "required": True},
                {"attr": "Operating System", "required": True},
                {"attr": "Battery", "required": True},
                {"attr": "Stylus Support", "required": False},
                {"attr": "Keyboard Included", "required": False},
            ],
            "Headphones": [
                {"attr": "Wireless", "required": True},
                {"attr": "Noise Cancellation", "required": False},
                {"attr": "Battery Life", "required": False},
                {"attr": "Driver Size", "required": False},
            ],
            "Clothing": [
                {"attr": "Size", "required": True},
                {"attr": "Color", "required": True},
                {"attr": "Material", "required": True},
                {"attr": "Gender", "required": True},
            ],
            "Shoes": [
                {"attr": "Shoe Size", "required": True},
                {"attr": "Color", "required": True},
                {"attr": "Shoe Type", "required": True},
                {"attr": "Gender", "required": True},
            ],
            "Watches": [
                {"attr": "Watch Type", "required": True},
                {"attr": "Water Resistant", "required": False},
                {"attr": "Strap Material", "required": True},
                {"attr": "Gender", "required": True},
            ],
            "Sport Equipment": [
                {"attr": "Sport Type", "required": True},
                {"attr": "Suitable For", "required": True},
            ],
        }

        for category_name, attribute_list in category_attribute_mapping.items():
            category = created_categories[category_name]
            self.stdout.write(f"\n  Category: {category_name}")
            for attr_config in attribute_list:
                attr_name = attr_config["attr"]
                is_required = attr_config["required"]
                attribute = created_attributes[attr_name]

                CategoryAttribute.objects.create(
                    category=category, attribute=attribute, is_required=is_required
                )
                required_text = "(required)" if is_required else "(optional)"

                self.stdout.write(f"Linked: {attr_name} {required_text}")
        self.stdout.write(self.style.SUCCESS("All category-attribute links created!"))

        self.stdout.write(self.style.SUCCESS("SETUP COMPLETE!"))
