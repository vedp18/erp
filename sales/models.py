from django.db import models
from django.conf import settings
from helper import phone_number_regex
from inventory.models import Item

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(
        max_length=16,
        validators=[phone_number_regex.phone_number_regex],
        unique=True
    )
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Customer: {self.name}"
    
class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sale_orders')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f"Sales Order: {self.id} - to Customer:{self.customer.name}"
    
    # --- State transition methods ---
    def confirm(self):
        if self.status != 'draft':
            raise ValueError("Only draft SOs can be confirmed.")
        self.status = 'confirmed'
        self.save(update_fields=['status'])

    def receive(self):
        if self.status != 'confirmed':
            raise ValueError("Only confirmed SOs can be delivered.")
        self.status = 'delivered'
        self.save(update_fields=['status'])

    def cancel(self):
        if self.status == 'delivered':
            raise ValueError("Delivered SOs cannot be cancelled.")
        self.status = 'cancelled'
        self.save(update_fields=['status'])
    
    

class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name="order_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity_ordered = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    sub_total = models.DecimalField(max_digits=20, decimal_places=2)

    def save(self, *args, **kwargs):
        self.sub_total = self.quantity_ordered * self.unit_price
        super().save(*args, **kwargs)

