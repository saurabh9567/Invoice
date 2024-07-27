from django.urls import path
from IIMS.views import  get_products_by_category, download_invoice

urlpatterns = [
    path('download-invoice/<int:invoice_id>/', download_invoice, name='generate_invoice'),
    path('get_products_by_category/<int:category_id>/', get_products_by_category, name='get_products_by_category'),

]