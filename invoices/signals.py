from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from sales.models import SalesOrder
from .models import Invoice, InvoiceItem
from .tasks import send_invoice_email

@receiver(post_save, sender=SalesOrder)
def create_invoices_for_sales_order(sender, instance, created, **kwargs):
    if instance.status == 'confirmed':
        # if no invoice exists yet
        if not hasattr(instance, 'invoice'):
            total = 0
            invoice = Invoice.objects.create(
                order_details=instance,
                total_amount = 0
            )
            for soi in instance.order_items.all():
                sub_total = soi.quantity_ordered * soi.unit_price
                InvoiceItem.objects.create(
                    invoice=invoice,
                    item = soi.item,
                    unit_price = soi.unit_price,
                    quantity_ordered = soi.quantity_ordered,
                    sub_total = soi.sub_total 
                )
                total += sub_total
            print(f"total: {total}")
            invoice.total_amount = total
            invoice.save()
            send_invoice_email.delay(invoice.id)


@receiver(pre_delete, sender=SalesOrder)
def cancel_invoice_on_salesorder_delete(sender, instance, **kwargs):
    """
    Before a SalesOrder is deleted, cancel its invoice
    if the invoice is still pending.
    """
    try:
        invoice = instance.invoice  # OneToOne relation
        if invoice.status == "pending":
            invoice.status = "cancelled"
            invoice.save()
    except Invoice.DoesNotExist:
        pass


@receiver(post_save, sender=SalesOrder)
def cancel_invoice_on_salesorder_status_change(sender, instance, **kwargs):
    """
    If SalesOrder status becomes 'cancelled',
    update its invoice status to cancelled (if still pending).
    """
    if instance.status == "cancelled":
        try:
            invoice = instance.invoice
            if invoice.status == "pending":
                invoice.status = "cancelled"
                invoice.save()
        except Invoice.DoesNotExist:
            pass
