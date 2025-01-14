from django.urls import path
from . import views

app_name = 'twitter'

urlpatterns = [
    path('', views.home, name='home'),
    path('profiles/', views.profiles , name='profiles'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('follow-unfollow/<int:pk>/', views.follow_unfollow, name='follow_unfollow'), # this url follow or unfollow a user
    path('login/', views.login_user , name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name="register"),
    path('update-user/', views.update_user , name="update_user"),
    path('update-profile/', views.update_profile , name="update_profile"),
    path('like-tweet/<int:pk>/', views.like_tweet, name='like_tweet'),
    path('share-tweet/<int:pk>/', views.share_tweet, name='share_tweet'),
    path('delete-tweet/<int:pk>/', views.delete_tweet, name='delete_tweet'),
    path('edit-tweet/<int:pk>/', views.edit_tweet, name="edit_tweet"),
]