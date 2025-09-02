from django.contrib import admin

from .models import Customer, SalesOrder, SalesOrderItem

class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "created_on", "status")
    actions = ['mark_as_confirmed', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    inlines = [SalesOrderItemInline]

    def mark_as_confirmed(self, request, queryset):
        for so in queryset:
            so.confirm()
    mark_as_confirmed.short_description = "Mark selected SOs as Confirmed"

    def mark_as_shipped(self, request, queryset):
        for so in queryset:
            so.ship()
    mark_as_shipped.short_description = "Mark selected SOs as Shipped"

    def mark_as_delivered(self, request, queryset):
        for so in queryset:
            so.deliver()
    mark_as_delivered.short_description = "Mark selected SOs as Delivered"

    def mark_as_cancelled(self, request, queryset):
        for so in queryset:
            so.cancel()
    mark_as_cancelled.short_description = "Cancel selected SOs"

admin.site.register(Customer)
