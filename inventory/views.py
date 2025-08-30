from rest_framework import viewsets
from .serializers import CategorySerializer
from users.permissions import IsAdmin, IsInventoryManager

from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsInventoryManager | IsAdmin]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAdmin | IsInventoryManager]

