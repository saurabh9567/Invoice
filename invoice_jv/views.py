import os
from django.http import HttpResponse, JsonResponse
from invoice_jv.models import Invoice, Product
from invoice.settings import STATIC_ROOT
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from num2words import num2words
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(STATIC_ROOT, 'admin', 'font', 'dejavu-sans', 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', os.path.join(STATIC_ROOT, 'admin', 'font', 'dejavu-sans', 'DejaVuSans-Bold.ttf')))


def get_products_by_category(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    products_data = [{'id': product.id, 'name': product.name} for product in products]
    return JsonResponse({'products': products_data})


def download_invoice(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    # Customer details
    customer_name = invoice.customer.name
    mobile_num = invoice.customer.mobile_no
    invoice_date = invoice.date.strftime('%Y-%m-%d')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice_id}_{invoice_date}.pdf"'

    border_padding = 20  # Padding for the border
    content_width = letter[0] - 2 * border_padding  # Calculate the content width
    footer_padding = 2  # Additional padding from the bottom border

    doc = SimpleDocTemplate(response, pagesize=letter,
                            leftMargin=border_padding, rightMargin=border_padding, topMargin=80, bottomMargin=80)
    styles = getSampleStyleSheet()
    elements = []

    # Header, footer, and border function
    def header_footer(canvas, doc):
        # Header
        canvas.saveState()
        
        # GST No. at top left corner
        canvas.setFont('Helvetica', 12)
        canvas.drawString(border_padding + 10, letter[1] - border_padding - 20, "GST No.: 09AFEPV3321C1Z0")
        canvas.drawRightString(letter[0] - border_padding - 10, letter[1] - border_padding - 20, "Mobile No.: 9897094388")
        canvas.drawRightString(letter[0] - border_padding - 10, letter[1] - border_padding - 35, f"Invoice No. {invoice_id}")
        
        canvas.setFont('Helvetica-Bold', 16)
        # Title in the center
        canvas.drawCentredString(letter[0] / 2, letter[1] - border_padding - 30, "Swarajya Singh Verma")
        
        # Address in the center, split into two lines
        address_line1 = "We offer a range of jewellery boxes, jewellery making tools, and acid."
        address_line2 = "96 Homganj Etawah (U.P.) 206001"
        bill_type = "ESTIMATE"
        
        canvas.setFont('Helvetica', 12)
        canvas.drawCentredString(letter[0] / 2, letter[1] - border_padding - 50, address_line1)
        canvas.drawCentredString(letter[0] / 2, letter[1] - border_padding - 65, address_line2)
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawCentredString(letter[0] / 2, letter[1] - border_padding - 90, bill_type)
        canvas.restoreState()

        # Footer
        canvas.saveState()
        footer_height = 0.45 * inch  # Footer height
        footer_y = border_padding + footer_padding  # Adjust footer y position to fit within the border
        
        # Draw footer background
        canvas.setFillColor(colors.grey)  # Gray color for footer background
        canvas.rect(border_padding, footer_y, content_width, footer_height, fill=1)  # Draw background

        # Draw footer text
        canvas.setFillColor(colors.white)  # Set text color to white
        canvas.setFont('Helvetica-Bold', 10)
        canvas.drawString(border_padding + 10, footer_y + 5, "")
        canvas.drawString(border_padding + 10, footer_y + 20, "")
        canvas.drawString(border_padding + 10, footer_y + 35, "")  # Adjusted position for more space
        canvas.drawRightString(letter[0] - border_padding - 10, footer_y + 15, "Name: Mr. Gaurav Verma")
        canvas.restoreState()

        # Border
        canvas.saveState()
        width, height = letter

        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(2)
        canvas.rect(border_padding, border_padding, width - 2 * border_padding, height - 2 * border_padding)
        canvas.restoreState()


    # Customer details as table rows
    customer_data = [
        ['Customer Name:', customer_name.title()],
        ['Mobile No.:', mobile_num],
        ['Date:', invoice_date],
    ]

    customer_table = Table(customer_data, colWidths=[1.5 * inch, content_width - 1.5 * inch])
    customer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    elements.append(Spacer(1, 30))
    elements.append(customer_table)
    elements.append(Spacer(1, 12))

    # Table Data with SNo column
    data = [['S.No', 'Product', 'Quantity', 'Unit Price', 'Total Price']]
    for idx, item in enumerate(invoice.items.all(), start=1):
        data.append([idx, item.product.name, item.quantity, f"₹{item.product.selling_price:.2f}", f"₹{item.total_price():.2f}"])

    # Add total amount in words row
    total_amount_words = num2words(invoice.total_amount(), lang='en_IN')

    # Add total amount row
    data.append([f'{total_amount_words.title()} Rupees Only.', '', '', 'Total', f"₹{invoice.total_amount():.2f}"])

    # Create the table
    table = Table(data, colWidths=[0.5 * inch, content_width - 0.5 * inch - 1.5 * inch - 1.5 * inch - 2 * inch, 1.5 * inch, 1.5 * inch, 2 * inch])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 13),
        ('TOPPADDING', (0, 0), (-1, -1), 13),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.grey),  # Total Amount row background
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),  # Total Amount row text color
        ('FONTNAME', (0, -1), (-1, -1), 'DejaVuSans-Bold'),  # Total Amount row font
        ('SPAN', (0, -1), (2, -1)),  # Merge cells for total_amount_in_words
        ('ALIGN', (0, -1), (2, -1), 'LEFT'),  # Left align total_amount_in_words
        ('ALIGN', (3, -1), (3, -1), 'CENTER'),  # Right align "Total" text
        ('ALIGN', (4, -1), (4, -1), 'CENTER'),  # Right align the actual amount
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Border for the whole table
    ]))

    elements.append(table)

    # Build the PDF with header, footer, and border
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)

    return response
