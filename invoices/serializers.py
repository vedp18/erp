from rest_framework import serializers
from .models import Invoice
from sales.serializers import SalesOrderSerializer

class InvoiceSerializer(serializers.ModelSerializer):
    order_details = SalesOrderSerializer()
    class Meta:
        model = Invoice
        fields = [
            'id',
            'order_details',
            'issued_on',
            'due_date',
            'total_amount',
            'status'
        ]