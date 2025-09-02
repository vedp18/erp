from rest_framework import viewsets
from .serializers import InvoiceSerializer
from .models import Invoice
from users.permissions import IsAdmin, IsSalesManager
from django.shortcuts import render, get_object_or_404


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdmin | IsSalesManager]


def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, "invoices/invoice_detail.html", {"invoice": invoice})



from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type="application/pdf")
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error creating PDF", status=400)
    return response

def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render_to_pdf("invoices/invoice_detail.html", {"invoice": invoice})
