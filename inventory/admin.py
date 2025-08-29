from django.contrib import admin

from .models import Category, Item, Stock

class StockInline(admin.StackedInline):
    model = Stock


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "sku", "unit", "category"]
    search_fields = ["name", "sku"]
    list_filter = ["category"]
    inlines = [StockInline]

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["id", "item", "quantity_available", "updated_on"]
    search_fields = ["item__name", "item__sku"]
    list_filter = ["updated_on"]