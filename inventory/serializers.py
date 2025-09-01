from rest_framework import serializers
from .models import Category, Item

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    class CategoryNameAndIdSerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ["id", "name"]

    category = CategoryNameAndIdSerializer(read_only=True)
    # category_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all(), source='category', write_only=True
    #     )
    category = serializers.JSONField(write_only=True, required=True)

    class Meta:
        model = Item
        fields = [
            "id", "name", "sku", "stock_available", "unit", "description",
            "category",     # for GET method
            # "category_id"   # for POST, PUT, PATCH methods or setting category field    
            ]
    
    def create(self, validated_data):
        category_data = validated_data.pop('category')

        # Case 1: Existing Category by ID
        if "id" in category_data:
            try:
                category = Category.objects.get(id=category_data["id"])
            except Category.DoesNotExist:
                raise serializers.ValidationError({"Category": "Category with this ID does not exist."})

        # Case 2: New category creation
        else:
            category = Category.objects.create(**category_data)

        # Attach category to purchase order item category
        validated_data["category"] = category
        return super().create(validated_data)

    def update(self, instance, validated_data):
        category_data = validated_data.pop("category", None)

        if category_data:
            if "id" in category_data:
                try:
                    category = Category.objects.get(id=category_data["id"])
                except Category.DoesNotExist:
                    raise serializers.ValidationError({"category": "Category with this ID does not exist."})
            else:
                category = Category.objects.create(**category_data)

            instance.category = category

        return super().update(instance, validated_data)

