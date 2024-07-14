from django import forms
from IIMS.models import InvoiceItem, Category, Product

class IIMSInvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['category', 'product', 'quantity']

    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True)
    quantity = forms.IntegerField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        # Add custom validation logic here if needed
        return cleaned_data
