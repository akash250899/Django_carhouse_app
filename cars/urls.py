from django.urls import path
from .views import cars, car_detail

app_name = 'cars'

urlpatterns = [
    path('', cars, name="home"),
    path('car/<int:pk>/', car_detail, name="car_detail"),
]