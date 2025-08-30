from django.contrib import admin

from .models import Supplier, PurchaseOrder, PurchaseOrderItem

class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "supplier", "created_on", "status")
    actions = ['mark_as_confirmed', 'mark_as_received', 'mark_as_cancelled']
    inlines = [PurchaseOrderItemInline]

    def mark_as_confirmed(self, request, queryset):
        for po in queryset:
            po.confirm()
    mark_as_confirmed.short_description = "Mark selected POs as Confirmed"

    def mark_as_received(self, request, queryset):
        for po in queryset:
            po.receive()
    mark_as_received.short_description = "Mark selected POs as Received"

    def mark_as_cancelled(self, request, queryset):
        for po in queryset:
            po.cancel()
    mark_as_cancelled.short_description = "Cancel selected POs"

admin.site.register(Supplier)
