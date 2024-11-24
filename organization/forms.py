from django import forms
from .models import Organization, CustomUser, Role
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'address', 'is_main']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']

class RoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=10,  # Restrict to 10 characters
        required=True,
        help_text="Required. Up to 10 characters. Letters, digits and @/./+/-/_ only.",
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'organization']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 10:
            raise ValidationError("Username must not exceed 10 characters.")
        return username