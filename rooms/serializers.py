from rest_framework import serializers
from .models import Rooms, RoomImage , OccupiedDate

class RoomImageSerializer(serializers.ModelSerializer):
    room = serializers.HyperlinkedRelatedField(view_name = "room-detail",queryset=Rooms.objects.all())
    class Meta:
        model = RoomImage
        fields = ["id","room","image","caption"]

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    class Meta:
        model = Rooms 
        fields = [
            'url',
            'id',
            'name',
            'type',
            'pricePerNight',
            'currency',
            'maxOccupancy',
            'description',
            'is_created',
            'is_updated',
            'images'
        ]
        extra_kwargs = {
            'url': {'view_name': 'room-detail'}
        }


class OccupiedDateSerializer(serializers.HyperlinkedModelSerializer):
    room = serializers.HyperlinkedRelatedField(
        view_name = 'room-detail', 
        queryset = Rooms.objects.all()
    )
    class Meta:
        model = OccupiedDate
        fields = ["url","id","room","date"]

