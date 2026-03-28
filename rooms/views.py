from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from .models import Rooms
from .serializers import RoomSerializer

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
