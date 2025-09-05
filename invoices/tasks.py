from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
from .models import Invoice


@shared_task
def send_invoice_email(invoice_id):
    try:
        invoice = Invoice.objects.select_related(
            "order_details__customer"
        ).prefetch_related(
            "order_items__item"
        ).get(id=invoice_id)

        customer = invoice.order_details.customer

        if not customer.email:
            return f"Customer {customer.name} has no email ID"

        # Render invoice HTML
        html_string = render_to_string("invoices/invoice_detail.html", {
            "invoice": invoice,
        })

        # Generate PDF with xhtml2pdf
        pdf_file = io.BytesIO()
        pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)

        if pisa_status.err:
            return f"Error generating PDF for Invoice {invoice.id}"

        pdf_file.seek(0)

        # Compose Email
        subject = f"Invoice #{invoice.id} - Your Order"
        body = render_to_string("emails/invoice_email.html", {
            "invoice": invoice,
            "customer": customer
        })
        email = EmailMessage(subject, body, to=[customer.email])
        email.content_subtype = "html"  # send as HTML email

        # Attach PDF
        email.attach(f"invoice_{invoice.id}.pdf", pdf_file.read(), "application/pdf")
        email.send()

        return f"Invoice {invoice.id} sent to {customer.email}"

    except Invoice.DoesNotExist:
        return f"Invoice {invoice_id} not found"
