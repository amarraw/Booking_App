from rest_framework import serializers
from .models import Rooms, RoomImage , OccupiedDate , User

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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = OccupiedDate
        fields = ["url","id","room","date","user"]

from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User 
        fields = ['url','id','username','password','email','full_name']

    def validate_password(self,value):
        return make_password(value)

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'full_name']

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)  # ✅ best practice
#         user.save()
#         return user