from django.urls import path
from .views import  get_products_by_category

urlpatterns = [
    # path('generate_invoice_pdf/<int:invoice_id>/', generate_invoice_pdf, name='generate_invoice_pdf'),
    path('get_products_by_category/<int:category_id>/', get_products_by_category, name='get_products_by_category'),

]