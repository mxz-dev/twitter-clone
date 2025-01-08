from django import forms
from django.contrib.auth.forms import UserCreationForm
from twitter.models import Tweets, Profile
from django.contrib.auth.models import User
class FollowForm(forms.Form):
    follow = forms.CharField(required=True, max_length=10)

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweets
        fields = ['tweet']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email","username", "password",)

class UserAvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ("avatar",)