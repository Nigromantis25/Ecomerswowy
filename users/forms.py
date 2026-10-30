from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Correo o nombre de usuario",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                try:
                    account = User.objects.get(username__iexact=email)
                except User.DoesNotExist:
                    account = None
                if account is not None:
                    user = authenticate(username=account.email, password=password)
            if user is None:
                raise ValidationError("Invalid username/email or password.")
            self.user = user  # Store the user for get_user method
        elif not email or not password:
            raise ValidationError("Enter a username/email and password.")
            
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        validators=[UnicodeUsernameValidator()],
    )
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("name", "username", "email", "phone", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if get_user_model().objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already registered.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if get_user_model().objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone
