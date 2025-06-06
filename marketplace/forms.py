from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import ClothingItem, ShippingAddress

class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        fields = ['title', 'age_group' , 'description', 'price', 'category', 'condition', 'size', 'image', 'is_featured']

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        "placeholder": "Enter your email",
        "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Enter your password",
        "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
    }))

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "placeholder": "Enter your email",
        "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
    }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        "placeholder": "Enter your password",
        "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
    }))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm your password",
        "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Enter your username",
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-input'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'state': forms.TextInput(attrs={'class': 'form-input'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input'}),
            'country': forms.TextInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
        }