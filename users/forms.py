"""
Forms for user authentication and profile management.
"""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django.forms import TextInput, Select, EmailInput, PasswordInput


class CustomUserCreationForm(UserCreationForm):
    """
    Form for new user registration (Sign Up).

    Includes validation for NRIC and Role fields.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username', 'password1', 'password2', 'nric_fin', 'role')
        
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control', 'id':'signup-email'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'id':'signup-first-name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'id':'signup-last-name'}),
            'username': TextInput(attrs={'class': 'form-control', 'id':'signup-username'}),
            'nric_fin': TextInput(attrs={'class': 'form-control', 'id':'signup-nric'}),
            'role': Select(attrs={'class': 'form-select', 'id':'signup-role'}),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initializes the form and applies CSS classes to password fields.
        """
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'id': 'signup-password1'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'id': 'signup-password2'})


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating existing user profiles.
    """
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username', 'password', 'nric_fin', 'role')
        
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
            'nric_fin': TextInput(attrs={'class': 'form-control'}),
            'role': Select(attrs={'class': 'form-select'}),
        }


class CustomLoginForm(AuthenticationForm):
    """
    Form for user login with custom styling.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'id': 'login-username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'id': 'login-password'})
