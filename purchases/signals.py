from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from .models import PurchaseOrder, PurchaseOrderItem
from inventory.models import Item

@receiver(post_save, sender=PurchaseOrder)
def update_stock_and_prices_on_receive_PO(sender, instance, **kwargs):
    if instance.status == "received":
        for poi in instance.order_items.all():
            item = Item.objects.get_or_create(item=poi.item)
            update_purchase_price(item, poi.unit_price, poi.quantity_ordered)
            item.stock_available += poi.quantity_ordered
            item.save()


def update_purchase_price(item, new_price, quantity):
    if new_price != item.purchase_price:
        total_cost = (item.purchase_price * item.stock_available) + (new_price * quantity)
        total_qty = item.stock_available + quantity
        item.purchase_price = total_cost / total_qty
        # item.stock_available += quantity
        # item.save()
