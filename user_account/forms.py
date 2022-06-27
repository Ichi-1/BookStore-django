from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import (
    AuthenticationForm, 
    SetPasswordForm,
    PasswordResetForm,  
)

from .models import CustomUser


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=255, widget=forms.TextInput(
        attrs={
            'class':'form-control mb-3',
            'placeholder': 'Enter your email',
            'id':'form-email',
        }
    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = CustomUser.objects.filter(email=email)
        if not user:
            raise ValidationError(
                f'Sorry, we can not find {email} address'
            )
        return email


class SetNewPassWordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3', 
                'placeholder': 'New Password', 
                'id': 'form-newpass',
            }
        ))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3', 
                'placeholder': 'New Password', 
                'id': 'form-new-pass2'
            }
        ))



    



class UserAccountUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label='Account email (can not be changed)',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class':'form-contril mb3',
            'placeholder': 'email',
            'id':'form-email',
            'readonly':'readonly',
        })
    )
    first_name = forms.CharField(
        label='Firstname',
        min_length=4,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class':'form-contril mb3',
            'placeholder': 'Firstname',
            'id':'form-firstname',
        })
    )


    class Meta:
        model = CustomUser
        fields = ('email', 'first_name')
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        label='Enter Username',
        min_length=5,
        max_length=50,
    )
    email = forms.EmailField(
        max_length=100,
        error_messages={'required': 'Email is required to sign up'}
    )
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = CustomUser.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username


    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Please use another Email, that is already taken')
        return email


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Passwords do not match.')
        return cd['password2']



    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-3', 
            'placeholder': 'Username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control mb-3', 
            'placeholder': 'E-mail', 
            'name': 'email', 
            'id': 'id_email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control mb-3',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Repeat Password'
        })


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-3', 
            'placeholder': 'Username', 
            'id': 'login-username'
        }
    ))
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))












