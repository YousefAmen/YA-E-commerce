from django import forms
from .models import (
    Category,
    Contact,
    Phone,
    Laptop,
    Tablet,
    Headphone,
    Clothing,
    Shoe,
    Watch,
    SportEquipment,
    ProductImage,
    Inventory,
)

exclude = [
    "merchant",
    "category",
    "favourites",
    "views",
    "slug",
    "views_number",
    "visitors",
    "created_at",
    "updated_at",
]


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        exclude = exclude
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe your phone..."}
            ),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
            "discount_price": forms.NumberInput(attrs={"step": "0.01"}),
        }


class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        exclude = exclude
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe your laptop..."}
            ),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
            "discount_price": forms.NumberInput(attrs={"step": "0.01"}),
        }


class TabletForm(forms.ModelForm):
    class Meta:
        model = Tablet
        exclude = exclude
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe your tablet..."}
            ),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
            "discount_price": forms.NumberInput(attrs={"step": "0.01"}),
        }


class HeadphoneForm(forms.ModelForm):
    class Meta:
        model = Headphone
        exclude = exclude
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe your headphones..."}
            ),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
            "discount_price": forms.NumberInput(attrs={"step": "0.01"}),
        }


class ClothingForm(forms.ModelForm):
    class Meta:
        model = Clothing
        exclude = exclude
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe the clothing item..."}
            ),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
            "discount_price": forms.NumberInput(attrs={"step": "0.01"}),
        }


class ShoeForm(forms.ModelForm):
    class Meta:
        model = Shoe
        exclude = exclude
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe the shoes..."}
            ),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
            "discount_price": forms.NumberInput(attrs={"step": "0.01"}),
        }


class WatchForm(forms.ModelForm):
    class Meta:
        model = Watch
        exclude = exclude
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe the watch..."}
            ),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
            "discount_price": forms.NumberInput(attrs={"step": "0.01"}),
        }


class SportEquipmentForm(forms.ModelForm):
    class Meta:
        model = SportEquipment
        exclude = exclude
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe the equipment..."}
            ),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
            "discount_price": forms.NumberInput(attrs={"step": "0.01"}),
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
            print(f"=------------------{ext}=-------------------")
            # raise forms.ValidationError(
            #     f"Only {', '.join(allowed_formats).upper()} formats are allowed"
            # )
        # if image.size > 5 * 1024 * 1024:
        #     raise forms.ValidationError("Image size must be less than 5MB")
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


# Add_Category_Form forms
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


# contact us forms
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


PRODUCT_FORM_MAPPING = {
    "phone": PhoneForm,
    "laptop": LaptopForm,
    "tablet": TabletForm,
    "headphone": HeadphoneForm,
    "clothing": ClothingForm,
    "shoe": ShoeForm,
    "watch": WatchForm,
    "sport_equipment": SportEquipmentForm,
}


def get_product_form(model_name):
    """
    - this function i will used it to get the form of correct model
    - i pass to it the model name from views
    - the function will return the correct form class based on the model name that i pass it

    """
    print(model_name)
    return PRODUCT_FORM_MAPPING.get(model_name.lower())
