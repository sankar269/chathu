from django import forms
from .models import Customer
from .models import CustomerProfile, KidProfile
from django.core.exceptions import ValidationError


class KidProfileForm(forms.ModelForm):
    class Meta:
        model = KidProfile
        fields = ['name', 'avatar']


class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'email', 'username', 'password', 'DoB', 'phonenumber']
        widgets = {
            'password': forms.PasswordInput(),
            'DoB': forms.DateInput(attrs={'type': 'date'}),
        }

        def clean_username(self):
            username = self.cleaned_data.get('username').lower()  # Convert username to lowercase
            existing_user = Customer.objects.filter(username=username).exists()

            if existing_user:
                raise ValidationError("This username already exists. Please choose a different one.")
            elif not all(char.isalnum() or char in ['@'] for char in username):
                raise ValidationError("Username should contain only small letters, numbers, and @ (if desired).")
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomerProfileForm(forms.ModelForm):
    confirm_pin = forms.CharField(widget=forms.PasswordInput, label='Confirm PIN')
    pin = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomerProfile
        fields = ['name', 'pin', 'confirm_pin', 'avatar']

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get('pin')
        confirm_pin = cleaned_data.get('confirm_pin')

        if pin and confirm_pin and pin != confirm_pin:
            raise forms.ValidationError("PIN and Confirm PIN do not match.")

class PINVerificationForm(forms.Form):
    pin = forms.CharField(widget=forms.PasswordInput)


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)