from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from .models import PurchaseOrder, PurchaseOrderItem
from inventory.models import Item

@receiver(post_save, sender=PurchaseOrder)
def update_stock_on_receive_PO(sender, instance, **kwargs):
    if instance.status == "received":
        for poi in instance.order_items.all():
            item = Item.objects.get_or_create(item=poi.item)
            item.quantity_available += poi.quantity_ordered
            item.save()


