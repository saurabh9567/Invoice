from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .models import Invoice, Product


def get_products_by_category(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    products_data = [{'id': product.id, 'name': product.name} for product in products]
    return JsonResponse({'products': products_data})

def generate_invoice_pdf(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(f"Invoice #{invoice.id}", styles['Title']))
    elements.append(Paragraph(f"Customer: {invoice.customer.name}", styles['Normal']))
    elements.append(Paragraph(f"Email: {invoice.customer.email}", styles['Normal']))
    elements.append(Paragraph(f"Date: {invoice.date}", styles['Normal']))
    elements.append(Paragraph("<br/>", styles['Normal']))

    # Table Data
    data = [['Product', 'Quantity', 'Unit Price', 'Total Price']]
    for item in invoice.items.all():
        data.append([item.product.name, item.quantity, f"{item.product.price:.2f}", f"{item.total_price():.2f}"])

    # Add total amount row
    data.append(['', '', 'Total Amount', f"{invoice.total_amount():.2f}"])

    # Create the table
    table = Table(data, colWidths=[2.5*inch, 1*inch, 1*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Build the PDF
    doc.build(elements)

    return response
