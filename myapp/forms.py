from django import forms
from myapp.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('client', 'product', 'num_units')
        widgets = {
            'client': forms.RadioSelect(),
        }
        labels = {
            'num_units': 'Quantity',
            'client': 'Client Name',
        }


class InterestForm(forms.Form):
    CHOICES = [('1', 'Yes'), ('2', 'No')]
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    quantity = forms.IntegerField(label="Quantity", min_value=1)
    comments = forms.CharField(required=False, widget=forms.Textarea, label='Additional Comments')