from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from twitter.models import Profile, Tweets
from .forms import FollowForm

def home(request):
    tweets = Tweets.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'tweets': tweets})

def profile(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user__pk=pk)
        current_user_profile = request.user.profile
        tweets = Tweets.objects.filter(user=profile.user).order_by('-created_at')
        if request.method == 'POST':
            form = FollowForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['follow'] == 'follow':
                    current_user_profile.follows.add(profile)
                    current_user_profile.save()
                    messages.success(request, f'You are now following {profile.user.username}.')
                else:
                    current_user_profile.follows.remove(profile)
                    current_user_profile.save()
                    messages.success(request, f'You have unfollowed {profile.user.username}.')
        return render(request, 'twitter/profile.html', {'profile': profile, 'tweets': tweets})
    
def profiles(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user.id)
        return render(request, 'twitter/profiles.html', {'profiles': profiles})
    
    messages.error(request, 'You need to be logged in to view profiles.')
    return redirect(reverse('twitter:home'))