from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    name = forms.CharField(label='Product Name', widget=forms.TextInput(attrs={'class': 'form-control', }))
    slug = forms.CharField(label='Product Path', required=True, widget=forms.TextInput(attrs={'class': 'form-control', }))
    description = forms.CharField(label='Description', widget=forms.TextInput(attrs={'class': 'form-control', }))
    price = forms.DecimalField(label='Price', widget=forms.TextInput(attrs={'class': 'form-control', }))
    trial = forms.CharField(label='Trial', widget=forms.TextInput(attrs={'class': 'form-control', }))
    subscription_interval = forms.CharField(label='Subscription Interval', widget=forms.TextInput(attrs={'class': 'form-control', }))

    class Meta:
        model=Product
        fields = ['name','slug','description','price','trial','subscription_interval','img']