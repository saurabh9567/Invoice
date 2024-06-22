from django.contrib import admin
from .models import Customer, Product, Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]
    list_display = ('id', 'customer', 'date', 'total_amount')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')

admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Invoice, InvoiceAdmin)
