from django.urls import path
from .views import home, about, services, contact, team_detail, search

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('services/', services, name="services"),
    path('contact/', contact, name="contact"),
    path('team/<int:id>/', team_detail, name="team_detail"),
    path('search', search, name='search')
]