from django.urls import path
from .views import generate_invoice_pdf

urlpatterns = [
    path('generate_invoice_pdf/<int:invoice_id>/', generate_invoice_pdf, name='generate_invoice_pdf'),
]