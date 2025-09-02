from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, invoice_detail, invoice_pdf
from django.urls import path


router = DefaultRouter()

router.register(r'', InvoiceViewSet, basename='invoice')

urlpatterns = router.urls

urlpatterns += [
    path("invoice/<int:pk>/", invoice_detail, name='invoice_detail'),
    path("invoice/<int:pk>/pdf/", invoice_pdf, name="invoice_pdf"),
]