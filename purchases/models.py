from django.db import models
from django.conf import settings
from helper import phone_number_regex
from inventory.models import Item


# Supplier
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        validators=[phone_number_regex.phone_number_regex],
        max_length=16,
        unique=True
    )
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Supplier: {self.name}"
    

# Purchase Order
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled')
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_orders')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f"PO-{self.id} - from supplier {self.supplier.name}"

    # @property
    # def sub_total(self):
    #     return sum(item.total_price for item in self.items.all())
    # def save(self, *args, **kwargs):
    #     self.total = sum(item.sub_total for item in self.order_items.all())
    #     super().save(update_fields='total')

    def update_sub_total(self):
        total = sum(item.sub_total for item in self.order_items.all())
        self.total = total
        self.save(update_fields=['total'])
    
    # --- State transition methods ---
    def confirm(self):
        if self.status != 'draft':
            raise ValueError("Only draft POs can be confirmed.")
        self.status = 'confirmed'
        self.save(update_fields=['status'])

    def receive(self):
        if self.status != 'confirmed':
            raise ValueError("Only confirmed POs can be received.")
        self.status = 'received'
        self.save(update_fields=['status'])

    def cancel(self):
        if self.status == 'received':
            raise ValueError("Received POs cannot be cancelled.")
        self.status = 'cancelled'
        self.save(update_fields=['status'])
    
class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity_ordered = models.DecimalField(max_digits=10, decimal_places=2, default=1.0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=20, decimal_places=2,default=0)

    def __str__(self):
        return f"Item:{self.item.name} x {self.quantity_ordered} from Order:{self.purchase_order.id}"
    
    # @property
    # def total_price(self):
    #     return self.quantity_ordered * self.unit_price
    def save(self, *args, **kwargs):
        self.sub_total = self.quantity_ordered * self.unit_price
        super().save(*args, **kwargs)
    
    
