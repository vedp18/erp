from rest_framework import viewsets
from .models import Customer, SalesOrder, SalesOrderItem

from .serializers import CustomerSerializer, SalesOrderSerializer, SalesOrderItemSerializer
from users.permissions import IsAdmin, IsSalesManager

class CustomerViewSet(viewsets.ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdmin | IsSalesManager]


class SalesOrderViewSet(viewsets.ModelViewSet):

    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAdmin | IsSalesManager]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)