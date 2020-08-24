from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home),
    path('points', views.points),
    path('daily_report', views.daily_report),
    path('settings', views.settings),
    path('forgot', views.forgot),
    path('clockin', views.clockin),
    path('clockout', views.clockout)
]

