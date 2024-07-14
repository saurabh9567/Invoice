from django.http import HttpResponse, JsonResponse
from .models import Invoice, Product
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def get_products_by_category(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    products_data = [{'id': product.id, 'name': product.name} for product in products]
    return JsonResponse({'products': products_data})