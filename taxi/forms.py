from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_num = self.cleaned_data["license_number"]
        if not license_num[:3].isupper() or not license_num[:3].isalpha():
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not license_num[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits.")

        return license_num


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = ("model", "manufacturer", "drivers",)


class DriverLicenseUpdateForm(forms.ModelForm):
    license_number = forms.CharField(
        required=True,
        validators=[MaxLengthValidator(8), MinLengthValidator(8)]
    )

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_num = self.cleaned_data["license_number"]
        if not license_num[:3].isupper() or not license_num[:3].isalpha():
            raise ValidationError(
                "First 3 characters must be uppercase letters."
            )

        if not license_num[3:].isdigit():
            raise ValidationError("Last 5 characters must be digits.")

        return license_num
