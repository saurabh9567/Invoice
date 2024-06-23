from django import forms
from .models import InvoiceItem, Category

class InvoiceItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = InvoiceItem
        fields = ['category', 'product', 'quantity']
