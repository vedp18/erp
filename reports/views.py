from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
from sales.models import SalesOrder
from purchases.models import PurchaseOrder
from invoices.models import Invoice
from django.db.models import Sum

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    @action(detail=False, methods=["get"])
    def sales_summary(self, request):
        data = SalesOrder.objects.values("customer__name").annotate(
            total=Sum("total_amount")
        )
        return Response(data)

    @action(detail=False, methods=["get"])
    def purchase_summary(self, request):
        data = PurchaseOrder.objects.values("supplier__name").annotate(
            total=Sum("total_amount")
        )
        return Response(data)