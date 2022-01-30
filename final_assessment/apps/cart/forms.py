from apps.auction.models import Auction
from django import forms

class Address(forms.Form):
    street = forms.CharField(label='Ulica',widget=forms.TextInput())
    city = forms.CharField(label='Miasto',widget=forms.TextInput())
    post_code = forms.CharField(label='Kod Pocztowy',widget=forms.TextInput())