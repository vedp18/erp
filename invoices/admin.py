from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "order_details", "issued_on", "total_amount")
    inlines = [InvoiceItemInline]

admin.site.register(InvoiceItem)

