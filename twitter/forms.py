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
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email","username", "password1", "password2",)
class UserUpdateForm(forms.ModelForm):
    old_password = forms.CharField(required=False)
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email","username", "old_password","password1","password2")
    
    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        if self.cleaned_data["password1"] != "" and self.cleaned_data["password2"] != "" and self.cleaned_data["old_password"] != "":
            if user.check_password(self.cleaned_data["old_password"]):
                if self.cleaned_data["password1"] == self.cleaned_data["password2"]:
                    user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ("avatar","bio","website","instagram","facebook","x")