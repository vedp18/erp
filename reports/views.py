from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
from sales.models import SalesOrder
from purchases.models import PurchaseOrder
from inventory.models import Item
from django.db.models import Sum, ExpressionWrapper, F, DecimalField

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    @action(detail=False, methods=["get"])
    def sales_summary(self, request):
        total_expr = ExpressionWrapper(
            F("order_items__quantity_ordered") * F("order_items__unit_price"),
            output_field=DecimalField(max_digits=20, decimal_places=2)
        )

        data = (
            SalesOrder.objects.values("customer__name", "customer__email", "customer__phone_number", "created_on", "status")
            .annotate(total_amount=Sum(total_expr))
            .order_by("customer__name")
        )

        return Response(data)
    

    @action(detail=False, methods=["get"])
    def purchase_summary(self, request):
        total_expr = ExpressionWrapper(
            F("order_items__quantity_ordered") * F("order_items__unit_price"),
            output_field=DecimalField(max_digits=20, decimal_places=2)
        )

        data = (
            PurchaseOrder.objects.values("supplier__name", "created_by__role", "created_on", "status")
            .annotate(total_amount=Sum(total_expr))
            .order_by("supplier__name")
        )

        return Response(data)
    
    
    @action(detail=False, methods=["get"])
    def stock_summary(self, request):
        stock_value_expr = ExpressionWrapper(
            F("stock_available") * F("unit_price"),
            output_field=DecimalField(max_digits=20, decimal_places=2)
        )

        data = (
            Item.objects.values("category__name")
            .annotate(
                total_stock=Sum("stock_available"),
                total_value=Sum(stock_value_expr)
            )
            .order_by("category__name")
        )

        return Response(data)
    
    @action(detail=False, methods=["get"])
    def stock_items_summary(self, request):
        stock_value_expr = ExpressionWrapper(
            F("stock_available") * F("unit_price"),
            output_field=DecimalField(max_digits=20, decimal_places=2)
        )

        data = (
            Item.objects.values(
                "id",
                "name",
                "sku",
                "category__name",
                "stock_available",
                "unit",
                "unit_price"
            )
            .annotate(total_value=stock_value_expr)
            .order_by("category__name", "name")
        )

        return Response(data)
    
    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        threshold = request.query_params.get("threshold", 10)

        try:
            threshold = float(threshold)
        except ValueError:
            return Response({"error": "Threshold must be a number"}, status=400)

        items = Item.objects.filter(stock_available__lt=threshold).values(
            "id", "name", "sku", "stock_available", "unit", "unit_price"
        ).order_by('stock_available')

        return Response(items)

