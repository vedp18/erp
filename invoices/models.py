from django.db import models
from django.utils import timezone

from sales.models import SalesOrder
from inventory.models import Item

class Invoice(models.Model):
    INVOICE_STATUS = [
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('paid', 'Paid'),
    ]

    # invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=INVOICE_STATUS, default='pending')
    order_details = models.OneToOneField(SalesOrder, on_delete=models.SET_NULL, null=True, related_name='invoice')
    description = models.TextField(max_length=255, blank=True, null=True)
    
    issued_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"Invoice: {self.id}, ({self.get_status_display()})"
    

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True)
    quantity_ordered = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    sub_total = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"Invoice: {self.item.name}, with price: {self.unit_price}"

