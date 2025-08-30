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
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
        )

    class Meta:
        model = Item
        fields = [
            "id", "name", "sku", "stock_available", "unit", "description",
            "category",     # for GET method
            "category_id"   # for POST, PUT, PATCH methods or setting category field    
            ]
