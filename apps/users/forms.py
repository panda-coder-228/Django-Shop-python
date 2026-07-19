from django import  forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from apps.users.models import CustomerUser
from apps.core.forms.mixins import BootstrapFormMixin
from django.core.validators import MinLengthValidator

class LoginUserForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())


class UserRegistrationForm(BootstrapFormMixin, UserCreationForm):
    first_name = forms.CharField(label="Ім'я", max_length=20, validators=[MinLengthValidator(3)])
    last_name = forms.CharField(label="Призвище", max_length=20, validators=[MinLengthValidator(3)])
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"placeholder": "example@gmail.com"}))
    phone = forms.CharField(label="Телефон", widget=forms.TextInput(attrs={"placeholder": "+38 (067) 123-56-55"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повторіть пароль", widget=forms.PasswordInput())

    class Meta:
        model = CustomerUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
        )

class UserProfileForm(BootstrapFormMixin, UserChangeForm):
    class Meta:
        model = CustomerUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
            "birthday",
            "about",
        )
        widgets = {
            "about": forms.Textarea(attrs={"rows" :4, "class": "resize-none"}),
            "birthday": forms.DateInput(attrs={"type": "date"})
        }