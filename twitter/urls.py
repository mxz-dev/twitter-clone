from django.urls import path
from . import views

app_name = 'twitter'

urlpatterns = [
    path('', views.index, name='home'),
    path('profiles/', views.profiles , name='profiles'),
]