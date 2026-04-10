from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.views import APIView
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .models import Rooms, OccupiedDate, User
from .serializers import RoomSerializer, OccupiedDateSerializer, UserSerializer
from rest_framework.authtoken.models import Token


@api_view(['GET'])
def api_root(request, format=None):
    if not request.user.is_authenticated:
        return Response({
            "details":"Not autorized"
        }, status=401)
    return Response({
        'rooms': reverse('room-list', request=request),
    })

    
class RoomList(generics.ListCreateAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    

class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]


class OccupiedDateList(generics.ListCreateAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return OccupiedDate.objects.none()
        if not user.is_superuser and not user.is_staff:
            return OccupiedDate.objects.filter(user=user)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class OccupiedDateDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [IsAdminOrReadOnly]
    


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return User.objects.all()

        return User.objects.filter(id=user.id)


class UserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        if obj.id == user.id or user.is_staff or user.is_superuser:
            return obj

        raise PermissionDenied("You have no permission to access user details.")


# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise)

class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        self.response_data = {
            "user":{
                "id":user.id,
                "username":user.email,
                "email": user.email,
                "full_name": user.full_name
            },
            "token":token.key
        }

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(self.response_data)

class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(
                {
                    "error":"username or password are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(username=username,password=password)

        if user is None:
            raise AuthenticationFailed("Invalid username or password")
        
        token, created = Token.objects.get_or_create(user=user)
        
        # Get user list based on permissions
        if user.is_superuser or user.is_staff:
            users_list = User.objects.all()
        else:
            users_list = User.objects.filter(id=user.id)
        
        users_serializer = UserSerializer(users_list, many=True)
        
        return Response({
            "message": "Login successful",
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name
            },
            "users": users_serializer.data
        }, status=status.HTTP_200_OK)