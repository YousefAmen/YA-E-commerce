from .models import User, Merchant, Customer
from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .signals import user_signed_up


class SignUpForms(SignupForm):
    first_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your First Name"}
        ),
    )

    last_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Last Name"}
        ),
    )

    role = forms.ChoiceField(
        choices=User.Role.choices, widget=forms.Select(attrs={"class": "form-control"})
    )

    gender = forms.ChoiceField(
        choices=User.Gender.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    city = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
    )

    state = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
    )

    zipcode = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "ZIP Code"}
        ),
    )

    country = CountryField(blank_label="Select Country").formfield(
        widget=CountrySelectWidget(
            attrs={"class": "form-control", "size": "5", "placeholder": "Country"}
        ),
        required=False,
    )

    def save(self, request):
        user = super().save(request)
        data = self.cleaned_data

        user.role = data["role"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.gender = data["gender"]
        user.birth_date = data["birth_date"]
        user.city = data["city"]
        user.state = data["state"]
        user.zipcode = data["zipcode"]
        user.country = data["country"]
        user.save()

        user_signed_up.send(
            sender=user.__class__, user=user, signup_data={"role": data["role"]}
        )
        return user


class SelectRole(forms.Form):
    ROLE_CHOICES = [
        ("merchant", "Merchant"),
        ("customer", "Customer"),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="Select your account type",
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "role",
            "bio",
            "gender",
            "profile_image",
            "phone",
            "city",
            "state",
            "zipcode",
        ]


class MerchentForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = [
            "business_name",
            "store_description",
            "business_phone",
            "business_address",
        ]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["shipping_address", "phone"]
