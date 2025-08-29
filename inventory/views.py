from rest_framework import viewsets
from .serializers import CategorySerializer
from users.permissions import IsAdmin, IsInventoryManager

from .models import Category, Item, Stock
from .serializers import CategorySerializer, ItemSerializer, StockSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin, IsInventoryManager]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAdmin, IsInventoryManager]

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAdmin, IsInventoryManager]

