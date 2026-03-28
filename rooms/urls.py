from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('rooms/', views.RoomList.as_view(), name='room-list'),
    path('rooms/<int:pk>/', views.RoomDetail.as_view(), name='room-detail'),
    path('occupied-date/',views.OccupiedDateList.as_view(), name="occupieddate-list"),
    path('occupied-date/<int:pk>',views.OccupiedDateDetails.as_view(), name="occupieddate-detail")

]

urlpatterns = format_suffix_patterns(urlpatterns)