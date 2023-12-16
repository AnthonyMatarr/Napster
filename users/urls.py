from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path("", views.home, name="home"),
    path("logout", views.logout_view, name="logout_view"),
    path("distance", DistanceView.as_view(), name='my_distance_view'), 
    path("map", MapView.as_view(), name='my_map_view'), 
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('add-location/', views.add_location, name='add_location'),
    path('add-rating/', views.add_rating, name='add_rating'),
    path("<int:spot_id>/", views.detail, name="detail"), 
    path('feedback/<int:location_id>/', views.feedback, name='feedback'), 
    path('user_feedback/', views.user_feedback, name='user_feedback'),

]