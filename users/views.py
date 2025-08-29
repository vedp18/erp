from rest_framework import generics, permissions, viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .permissions import IsAdmin

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
