from rest_framework import serializers

from .models import Supplier, PurchaseOrder, PurchaseOrderItem
from inventory.models import Item

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class PurchaseOrderItemSerializer(serializers.ModelSerializer):

    class ItemNameAndIdSerializer(serializers.ModelSerializer):
        class Meta:
            model = Item
            fields = ['id', 'name']
    
    item = ItemNameAndIdSerializer()
    unit = serializers.CharField(source='item.unit', read_only=True)
    class Meta:
        model = PurchaseOrderItem
        fields = ['item', 'quantity_ordered', 'unit', 'unit_price', 'sub_total']
        read_only_fields = ['sub_total']


class PurchaseOrderSerializer(serializers.ModelSerializer):

    class SupplierNameAndIdSerializer(serializers.ModelSerializer):
        class Meta:
            model = SupplierSerializer
            fields = ['id', 'name']

    supplier = SupplierSerializer()
    order_items = PurchaseOrderItemSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'supplier', 'created_by', 'created_on', 'status', 'order_items', 'total']
    

    # for post, put
    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        po = PurchaseOrder.objects.create(**validated_data)
        for order_item in items_data:
            PurchaseOrderItem.objects.create(purchase_order=po, **order_item)
        return po
    

