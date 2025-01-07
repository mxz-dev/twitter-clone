from django import forms
from twitter.models import Tweets
class FollowForm(forms.Form):
    follow = forms.CharField(required=True, max_length=10)

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweets
        fields = ['tweet']