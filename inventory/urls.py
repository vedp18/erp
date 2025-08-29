from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ItemViewSet, StockViewSet

router = DefaultRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'items', ItemViewSet)
router.register(r'stock', StockViewSet)

urlpatterns = router.urls