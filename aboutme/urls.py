from django.contrib.auth import views as auth_views
from django.urls import path
from aboutme import views

app_name = 'aboutme'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile')
]