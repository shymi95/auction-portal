from apps.user_handler.models import CustomUser
from apps.auction.models import Auction
from django import forms
from apps.main.models import Categories

class Searchbox(forms.Form):
    search_key = forms.CharField(max_length=50, label=False, widget=forms.TextInput(attrs={'placeholder': 'Wyszukaj'}))
    

class AuctionForm(forms.ModelForm):
    # category = forms.ModelChoiceField(queryset=Categories.objects.all(),empty_label=None, to_field_name="category")
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_ID']=forms.ModelChoiceField(queryset=Categories.objects.all(),empty_label=None, to_field_name="category")
        self.fields['category_ID'].widget.attrs.update({'class': 'dropdown'})
        self.fields['description'].widget.attrs.update({'class': 'textarea'})

    class Meta:
        model = Auction
        exclude = ['buyer_ID', 'creator_ID', 'created', 'is_paid', 'current_price']
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'ends':forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'current_price':forms.TextInput()
            # 'ends_time': forms.TimeInput(attrs={'type': 'time'})
        }
        labels = {
            'current_price': 'Twoja cena:'
        }
    # def clean(self):
    #     cleaned_data = super().clean()
    #     cleaned_data['category_ID'] = Categories.objects.all().filter(category=).first()
    #     return cleaned_data


class AuctionUpdate(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['current_price'].widget.attrs.update({'class': 'bid_input'})

    class Meta:
        model = Auction
        fields = ['current_price']
        widgets = {
            'current_price':forms.TextInput()
        }
        labels = {
            'current_price': 'Twoja cena:'
        }
    

        




