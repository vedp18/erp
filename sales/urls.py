from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, SalesOrderViewSet


router = DefaultRouter()

router.register('customers', CustomerViewSet, basename='customers')
router.register('sales-orders', SalesOrderViewSet, basename='sales-orders')

urlpatterns = router.urls