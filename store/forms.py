from django import forms
from .models import (
    Category,
    CategoryAttribute,
    Contact,
    Product,
    ProductImage,
    Inventory,
)


class DaynamicProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ["product_model", "name", "description", "price", "discount"]

    def __init__(self, category_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if category_id:
            category = Category.objects.get(id=category_id)

            category_attributes = CategoryAttribute.objects.filter(category=category)

            for cat_attr in category_attributes:
                attribute = cat_attr.attribute
                field_name = f"attr_{attribute.id}"
                label = attribute.name
                if attribute.unit:
                    label = f"{attribute.name} ({attribute.unit})"

                if attribute.attribute_type == "text":
                    self.fields[field_name] = forms.CharField(
                        label=label,
                        required=cat_attr.is_required,
                        widget=forms.TextInput(
                            {"placeholder": f"Enter {attribute.name}"}
                        ),
                    )
                elif attribute.attribute_type == "number":
                    self.fields[field_name] = forms.DecimalField(
                        label=label,
                        required=cat_attr.is_required,
                        widget=forms.NumberInput(
                            attrs={"placeholder": f"Enter {attribute.name}"}
                        ),
                    )

                elif attribute.attribute_type == "boolean":
                    self.fields[field_name] = forms.ChoiceField(
                        label=label,
                        required=cat_attr.is_required,
                        choices=[("", "---"), ("Yes", "Yes"), ("No", "No")],
                        widget=forms.Select({"placeholder": f"Enter {attribute.name}"}),
                    )

                elif attribute.attribute_type == "choice":
                    self.fields[field_name] = forms.CharField(
                        label=label,
                        required=cat_attr.is_required,
                        widget=forms.TextInput(
                            attrs={"placeholder": f"Enter {attribute.name}"}
                        ),
                    )
                self.fields[field_name].attribute = attribute
                self.fields[field_name].is_attribute_field = True

        else:
            return ValueError("error Please you must send category")

    def get_attribute_fields(self):
        return {
            name: field
            for name, field in self.fields.items()
            if hasattr(field, "is_attribute_field")
        }

    def get_basic_fields(self):
        return {
            name: field
            for name, field in self.fields.items()
            if not hasattr(field, "is_attribute_field")
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image", "is_primary"]

    def clean_image(self):
        image = self.cleaned_data["image"]
        allowed_formats = ["jpg", "jpeg", "png", "webp"]
        ext = image.name.split(".")[-1].lower()

        if not image:
            raise forms.ValidationError("Please select an image")

        if ext not in allowed_formats:
            raise forms.ValidationError(
                f"Only {', '.join(allowed_formats).upper()} formats are allowed"
            )
        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image size must be less than 5MB")
        return image


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["quantity"]
        widgets = {
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control qty-input",
                    "id": "id_quantity",
                    "min": "0",
                    "value": "10",
                    "required": True,
                }
            )
        }


class Choosing_Category_Form(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter The Name Of Category",
                }
            ),
        }


class Contact_Us_Form(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Your Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter Your Email"}
            ),
            "subject": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter The Subject..."}
            ),
            "message": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter The Message..."}
            ),
        }


class AddCategoriesForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "parent", "description"]
