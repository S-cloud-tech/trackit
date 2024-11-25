from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate
from .models import Profile
class LoginForm(AuthenticationForm):
    email = forms.EmailField(label='Enter Email', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    # email = forms.EmailField(label='Enter Username', widget=forms.TextInput(attrs={'class':'form-control'}))
    # password = forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    # def confirm_login_allowed(self, user):
    #     if user.is_staff and not user.is_superuser:
    #         raise ValidationError(
    #             ("This account is not allowed here."),
    #             code='not_allowed',
    #         )
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'weight', 'height', 'profile_image', 'goals']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your weight (kg)'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your height (cm)'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'goals': forms.Select(attrs={'class': 'form-control'}),
        }