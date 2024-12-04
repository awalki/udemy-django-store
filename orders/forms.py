from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Смирнов'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@domain.com'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Улица Пушкина дом колотушкина'}))

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "email", "address")