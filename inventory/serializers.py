from rest_framework import serializers
from .models import Category, Item, Stock

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='item', write_only=True
    )

    class Meta:
        model = Stock
        fields = ["id", "item", "item_id", "quantity", "last_updated"]


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    # Accept stock data when creating an item
    stock = StockSerializer(write_only=True, required=False)
    stock_detail = StockSerializer(read_only=True, source="stock")  # to show stock in response

    class Meta:
        model = Item
        fields = ["id", "name", "sku", "unit", "description", "category", "category_id",
                  "stock",          # for setting stock with items
                  "stock_detail"    # for getting stock with items
                  ]
    def create(self, validated_data):
        stock_data = validated_data.pop("stock", None)
        item = Item.objects.create(**validated_data)

        if stock_data:
            Stock.objects.update_or_create(
                item=item,
                defaults={"quantity_available": stock_data.get("quantity_available", 0)}
            )

        # else -> signal will auto-create stock with 0
        return item

