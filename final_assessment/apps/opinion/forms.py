from django import forms
from apps.opinion.models import Opinions

class Opinion(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['buyer_grade'].widget.attrs.update({'class': 'dropdown'})
        self.fields['buyer_comment'].widget.attrs.update({'class': 'textarea'})

    class Meta:
        model = Opinions
        fields = ['buyer_grade', 'buyer_comment']
        widgets = {
            'buyer_grade':forms.Select(),
            'buyer_comment': forms.Textarea()
        }
        labels = {
            'buyer_grade': 'Twoja ocena:',
            'buyer_comment': 'Twój komentarz:'
        }