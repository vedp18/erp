from rest_framework import serializers

from .models import Supplier, PurchaseOrder, PurchaseOrderItem
from inventory.models import Item

from inventory.serializers import ItemSerializer

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    # Will return {id, name} for GET
    item_data = serializers.SerializerMethodField(read_only=True)

    # Accepts dict for POST/PUT
    item = serializers.JSONField(write_only=True, required=True)

    unit = serializers.CharField(source='item.unit', read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = [
            'item_data',    # for GET
            'item',         # for POST/PUT
            'quantity_ordered',
            'unit',         # for GET
            'unit_price',
            'sub_total'
        ]
        read_only_fields = ['sub_total']

    def get_item_data(self, obj):
        return {
            "id": obj.item.id,
            "name": obj.item.name
        }

    def create(self, validated_data):
        item_data = validated_data.pop("item")

        # Case 1: Existing item by ID
        if "id" in item_data:
            try:
                item = Item.objects.get(id=item_data["id"])
            except Item.DoesNotExist:
                raise serializers.ValidationError({"item": "Item with this ID does not exist."})

        # Case 2: New item creation
        else:
            # item = Item.objects.create(**item_data)
            item_serializer = ItemSerializer(data=item_data)
            item_serializer.is_valid(raise_exception=True)
            item = item_serializer.save()

        # Attach item to purchase order item
        validated_data["item"] = item
        return super().create(validated_data)

    def update(self, instance, validated_data):
        item_data = validated_data.pop("item", None)

        if item_data:
            if "id" in item_data:
                try:
                    item = Item.objects.get(id=item_data["id"])
                except Item.DoesNotExist:
                    raise serializers.ValidationError({"item": "Item with this ID does not exist."})
            else:
                item = Item.objects.create(**item_data)

            instance.item = item

        return super().update(instance, validated_data)


class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier = serializers.SerializerMethodField()
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), source='supplier', write_only=True, required=False
    )
    supplier_name = serializers.CharField(write_only=True, required=False)
    order_items = PurchaseOrderItemSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 
                  'supplier',       # for GET method only
                  'supplier_id',    # for POST/PUT with existing supplier
                  'supplier_name',  # for POST/PUT with new supplier
                  'created_by', 'created_on', 'status', 'order_items', 'total']
        read_only_fields =  ['created_by', 'created_on', 'total']

    def get_supplier(self, obj):
        return {
            "id": obj.supplier.id,
            "name": obj.supplier.name
        }

    # for post, put
    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        supplier = validated_data.pop('supplier', None)  # already a Supplier object if supplier_id was sent
        supplier_name = validated_data.pop('supplier_name', None)

        if supplier is None and supplier_name:
            supplier = Supplier.objects.create(name=supplier_name)

        if supplier is None:
            raise serializers.ValidationError("Supplier info is required")

        po = PurchaseOrder.objects.create(supplier=supplier, **validated_data)

        for order_item_data in items_data:
            # use PurchaseOrderItemSerializer’s logic
            order_item_serializer = PurchaseOrderItemSerializer(data=order_item_data)
            order_item_serializer.is_valid(raise_exception=True)
            order_item_serializer.save(purchase_order=po)

        return po

    

