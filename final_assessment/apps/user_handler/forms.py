from django import forms

class Registration(forms.Form):
    email = forms.EmailField(label='Email',widget=forms.EmailInput())
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password',widget=forms.PasswordInput())

class Login(forms.Form):
    email = forms.EmailField(label='Email',widget=forms.EmailInput())
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
