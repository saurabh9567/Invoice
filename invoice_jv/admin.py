from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Customer, Category, Product, Invoice, InvoiceItem
from invoice_jv.forms import IIMSInvoiceItemForm
from django.contrib.admin.models import LogEntry
from invoice_jv.views import download_invoice
from django.urls import path
from django.shortcuts import get_object_or_404

class InvoiceItemInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        if not any(form.cleaned_data and not form.cleaned_data.get('DELETE', False) for form in self.forms):
            raise ValidationError("At least one invoice item is required.")

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    formset = InvoiceItemInlineFormset
    form = IIMSInvoiceItemForm
    extra = 1

    class Media:
        js = (
            'admin/js/jquery.init.js',
            'admin/js/invoice_jv_item.js',
        )

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]
    list_display = ('id', 'customer', 'date', 'total_amount', 'download_invoice')
    list_filter = ('date',)
    
    def save_model(self, request, obj, form, change):
    # Save the main object first to get a primary key
        if not obj.pk:
            super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        try:
            instances = formset.save(commit=False)
            if not instances:
                raise ValidationError("At least one invoice item is required.")
            for instance in instances:
                instance.save()
            formset.save_m2m()
        except ValidationError as e:
            formset._non_form_errors = formset.error_class([str(e)])
            messages.error(request, "Please fill all the required fields.")
            return

    def response_add(self, request, obj, post_url_continue=None):
        if not obj.items.exists():
            obj.delete()
            messages.error(request, "Please fill all the required fields.")
            return super().response_add(request, obj, post_url_continue)
        messages.success(request, "Invoice added successfully.")
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if not obj.items.exists():
            obj.delete()
            messages.error(request, "Please fill all the required fields.")
            return super().response_change(request, obj)
        messages.success(request, "Invoice updated successfully.")
        return super().response_change(request, obj)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('download-invoice/<int:invoice_id>/', self.admin_site.admin_view(self.download_invoice_view), name='download_invoice'),
        ]
        return custom_urls + urls

    def download_invoice_view(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        response = download_invoice(request, invoice_id)
        return response

    def download_invoice(self, obj):
        return format_html(
            '<a class="button" href="{}">Save</a>',
            reverse('admin:download_invoice', args=[obj.pk]),
        )
    download_invoice.short_description = 'Save'
    download_invoice.allow_tags = True

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'purchase_price', 'selling_price', 'quantity', 'category')
    list_filter = ('category',)

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Invoice, InvoiceAdmin)