from django.db import models

# Create your models here.

class Rooms(models.Model):
    ROOM_TYPE = [
        ("basic","Basic"),
        ("standard","Standard"),
        ("delux","Delux")
    ]
    CURRENCY_TYPE = [
        ("USD","USD"),
        ("EUR","EUR"),
    ]
    name = models.CharField(max_length=100, blank=True, default=" ")
    type = models.CharField(max_length=100, choices=ROOM_TYPE)
    pricePerNight = models.IntegerField(default=1500)
    currency = models.CharField(default="USD",max_length=10,choices=CURRENCY_TYPE)
    maxOccupancy = models.IntegerField(default=1)
    description = models.TextField()
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=True)


class RoomImage(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name="images")
    image =  models.ImageField(upload_to="room_image/")
    caption = models.CharField(max_length=100, blank=True, null=True)


    