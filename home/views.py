# views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, UserLoginSerializer

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'email': user.email,
            'role': user.role.role_name,
        }, status=status.HTTP_200_OK)


from rest_framework import generics, status
from rest_framework.response import Response
from .models import RoleMaster
from .serializers import RoleMasterSerializer
from rest_framework.permissions import IsAdminUser  # or custom permission class

class RoleMasterListView(generics.ListCreateAPIView):
    queryset = RoleMaster.objects.all()
    serializer_class = RoleMasterSerializer
    permission_classes = [IsAdminUser]  # Only admins can create roles

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoleMasterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoleMaster.objects.all()
    serializer_class = RoleMasterSerializer
    permission_classes = [IsAdminUser]  # Only admins can modify roles