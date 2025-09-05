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
    # Accept dict for POST method
    item = serializers.JSONField(write_only=True, required=True)

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
        read_only_fields = ['id', 'sub_total', ]

    def get_item_details(self, obj):
        return {
            'id': obj.item.id,
            'name': obj.item.name,
            'sku': obj.item.sku
        }
    
    def create(self, validated_data):
        item_data = validated_data.pop('item')

        # Case 1: Existing item by ID
        if "id" in item_data:
            try:
                item = Item.objects.get(id=item_data["id"])
            except Item.DoesNotExist:
                raise serializers.ValidationError({"item": "Item with this ID does not exist."})

        # Attach item to purchase order item
        validated_data["item"] = item
        return super().create(validated_data)

class SalesOrderSerializer(serializers.ModelSerializer):
    customer_details = CustomerSerializer(source='customer', read_only=True)
    customer = serializers.JSONField(write_only=True, required=True)
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
        customer_data = validated_data.pop('customer', None)
        try:
            # Case 1: Existing Customer with phone_number
            customer = Customer.objects.get(phone_number=customer_data['phone_number'])
        except Customer.DoesNotExist:
            # Case 2: New Customer creation
            if "name" in customer_data:
                # if customer does not exist then create new customer
                customer_serializer = CustomerSerializer(data=customer_data)
                customer_serializer.is_valid(raise_exception=True)
                customer = customer_serializer.save()
            else:
                raise serializers.ValidationError({"customer": "Customer with this id does not exist."})


        # # Case 1: Existing Customer with phone_number
        # if "phone_number" in customer_data:
        #     try:
        #         customer = Customer.objects.get(phone_number=customer_data['phone_number'])
        #     except Customer.DoesNotExist:
        #         raise serializers.ValidationError({"customer": "Customer with this id does not exist."})
        
        # # Case 2: New Customer creation
        # else:
        #     customer_serializer = CustomerSerializer(data=customer_data)
        #     customer_serializer.is_valid(raise_exception=True)
        #     customer = customer_serializer.save()

        sales_order = SalesOrder.objects.create(customer=customer, **validated_data)

        # Handle Item Data
        for item_data in items_data:
            # use PurchaseOrderItemSerializer’s logic
            sales_order_item_serializer = SalesOrderItemSerializer(data=item_data)
            sales_order_item_serializer.is_valid(raise_exception=True)
            sales_order_item_serializer.save(sales_order=sales_order)        

        return sales_order
    
    def update(self, instance, validated_data):
        items_data = validated_data.pop('order_items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()

            for item_data in items_data:
                SalesOrderItem.objects.create(sales_order=instance, **item_data)
        return instance
        

