from django import forms

class FollowForm(forms.Form):
    follow = forms.CharField(required=True, max_length=10)

    