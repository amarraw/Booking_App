from django.contrib import admin
from .models import Rooms, RoomImage

@admin.register(Rooms)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name","type"]
    search_fields = ["name"]
    list_filter = ["type"]

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ["room","image", "caption"]
    