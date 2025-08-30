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


@receiver([post_save, post_delete], sender=PurchaseOrder) 
def update_purchase_order_total(sender, instance, **kwargs):
    instance.update_sub_total()

# @receiver([post_save, post_delete], sender=PurchaseOrderItem)
# def update_purchase_order_total(sender, instance, **kwargs):
#     purchase_order = instance.purchase_order
#     purchase_order.total = purchase_order.order_items.aggregate(
#         total=Sum('sub_total')
#     )['total'] or 0
#     purchase_order.save(update_fields=['total'])
