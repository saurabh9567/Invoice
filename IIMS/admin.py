from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Customer, Category, Product, Invoice, InvoiceItem
from IIMS.forms import IIMSInvoiceItemForm
from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    form = IIMSInvoiceItemForm
    extra = 1

    class Media:
        js = (
            'admin/js/jquery.init.js',
            'admin/js/iims_invoice_item.js',
        )

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]
    list_display = ('id', 'customer', 'date', 'total_amount')
    list_filter = ('date',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    list_filter = ('category',)

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Invoice, InvoiceAdmin)
