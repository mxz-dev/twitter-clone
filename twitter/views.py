from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from twitter.models import Profile

def index(request):
    return render(request, 'home.html')

def profiles(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user.id)
        return render(request, 'twitter/profiles.html', {'profiles': profiles})
    
    messages.error(request, 'You need to be logged in to view profiles.')
    return redirect(reverse('twitter:home'))