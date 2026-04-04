from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from .models import Rooms, OccupiedDate
from .serializers import RoomSerializer, OccupiedDateSerializer

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
    permission_classes = [IsAuthenticated]
    

class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer


class OccupiedDateList(generics.ListCreateAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not  user.is_superuser and not user.is_staff:
            return OccupiedDate.objects.filter(user=user) 
        return super().get_queryset()
    

class OccupiedDateDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [IsAuthenticated]
