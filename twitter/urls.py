from django.urls import path
from . import views

app_name = 'twitter'

urlpatterns = [
    path('', views.home, name='home'),
    path('profiles/', views.profiles , name='profiles'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('login/', views.login_user , name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name="register"),
    path('update-user/', views.update_user , name="update_user"),
    path('like-tweet/<int:pk>/', views.like_tweet, name='like_tweet'),
    path('share-tweet/<int:pk>/', views.share_tweet, name='share_tweet'),
]