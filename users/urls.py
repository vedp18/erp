from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet

router = DefaultRouter()
router.register('users',UserViewSet)

urlpatterns = [
    path('auth/token/',TokenObtainPairView.as_view(), name="token_obtain_pair"),        # for login as user use GET 
    path('auth/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    # path('auth/users/', UserListView.as_view(), name="user_list"),
]

urlpatterns += router.urls