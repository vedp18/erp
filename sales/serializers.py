from rest_framework import serializers
from .models import Customer, SalesOrder, SalesOrderItem
from inventory.models import Item
from inventory.serializers import ItemSerializer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id", 'name', 'email', 'phone_number', 'address'
        ]
        read_only_fields = ['id']


class SalesOrderItemSerializer(serializers.ModelSerializer):
    item_details = serializers.SerializerMethodField(read_only=True)
    # item_details = ItemSerializer(source='item', read_only=True)
    item = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), write_only=True,
    )

    unit = serializers.CharField(source='item.unit', read_only=True)
    
    class Meta:
        model = SalesOrderItem
        fields = [
            'id',
            'item',         # for POST/PUT
            'item_details',    # for GET
            'quantity_ordered',
            'unit',
            'unit_price', 'sub_total'
        ]
        read_only_fields = ['id', 'sub_total']

    def get_item_details(self, obj):
        return {
            'id': obj.item.id,
            'name': obj.item.name,
            'sku': obj.item.sku
        }



class SalesOrderSerializer(serializers.ModelSerializer):
    customer_details = CustomerSerializer(source='customer', read_only=True)
    customer = serializers.JSONField(write_only=True, required=False)
    order_items = SalesOrderItemSerializer(many=True)

    class Meta:
        model = SalesOrder
        fields = [
            'id',
            'customer_details',    # for GET method
            'customer',            # for POST/PUT method
            'status', 'order_items', 'created_by', 'created_on',
        ]
        read_only_fields = ['created_by', 'created_on']

    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        sales_order = SalesOrder.objects.create(**validated_data)
        for item_data in items_data:
            SalesOrderItem.objects.create(sales_order=sales_order, **item_data)
        return sales_order
    
    def update(self, instance, validated_data):
        items_data = validated_data.pop('order_items')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()

            for item_data in items_data:
                SalesOrderItem.objects.create(sales_order=instance, **item_data)
            return instance
        

