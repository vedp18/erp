from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .permissions import IsAdmin

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


    def create(self, request, *args, **kwargs):
        try:
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(
                    {
                        'message': "User created successfully",
                        'success': True,
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    'error': user_serializer.errors,
                    'success': False,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'error': str(e),
                    'success': False,
                },
                status=status.HTTP_400_BAD_REQUEST
            )




    # def create(self, request, *args, **kwargs):
    #     try:
    #         try:
    #             user = User.objects.get(username=request.data['username'])
    #         except User.DoesNotExist:
    #             return Response(
    #                 {
    #                     'error': "User not Found",
    #                     'success': False,
    #                 },
    #                 status=status.HTTP_404_NOT_FOUND
    #             )
    #         if not user.check_password(request.data["password"]):
            
