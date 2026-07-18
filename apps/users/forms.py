from django import  forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from apps.users.models import CustomerUser
from apps.core.forms.mixins import BootstrapFormMixin

class LoginUserForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())