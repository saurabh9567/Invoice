from django import forms
from .models import InvoiceItem, Category, Product

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['category', 'product', 'quantity']

    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True)
    quantity = forms.IntegerField(required=True)
    
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')

        if product and quantity:
            if quantity > product.quantity:
                raise forms.ValidationError(f"Insufficient stock for {product.name}")
        return cleaned_data
