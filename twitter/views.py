from django.shortcuts import render
from twitter.models import Profile
def index(request):
    pass
    return render(request, 'home.html')

def profiles(request):
    profiles = Profile.objects.exclude(user=request.user.id)
    return render(request, 'twitter/profiles.html', {'profiles': profiles})