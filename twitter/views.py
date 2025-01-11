from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from twitter.models import Profile, Tweets
from .forms import FollowForm, TweetForm, UserUpdateForm, UserProfileUpdateForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.contrib.sites.shortcuts import get_current_site

def login_user(request):
    if request.user.is_authenticated == False:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect(reverse('twitter:home'))
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect(reverse('twitter:login'))
        return render(request, 'twitter/login.html')
    messages.error(request, 'You are already logged in.')
    return redirect(reverse('twitter:home'))

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect(reverse('twitter:home'))

def register_user(request):
    if request.user.is_authenticated == False:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created successfully.')
                return redirect(reverse('twitter:login'))
            else:
                messages.success(request, 'An error occurred during registration. Please try again.')
        return render(request, 'twitter/register.html')
    messages.error(request, 'You are already logged in.')
    return redirect(reverse('twitter:home'))

@login_required
def update_user(request):
    current_user = User.objects.get(id=request.user.id)
    current_user_profile = Profile.objects.get(user__id=request.user.id)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'Account updated successfuly.')
            return redirect(reverse('twitter:update_user'))
        else:
            messages.success(request, 'An error occured during Updating Account. Please try again.')
            return redirect(reverse('twitter:update_user'))
    return render(request, 'twitter/update_account.html', {"user":current_user}) 

@login_required
def update_profile(request):
    current_user_profile = Profile.objects.get(user__id=request.user.id)
    if request.method == "POST":
        profile_form = UserProfileUpdateForm(request.POST or None, request.FILES or None, instance=current_user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfuly.')
            return redirect(reverse('twitter:update_profile'))
        else:
            messages.success(request, 'An error occured during Updating Profile. Please try again.')
            return redirect(reverse('twitter:update_profile'))
    return render(request, 'twitter/update_profile.html', {"profile":current_user_profile}) 
    
def home(request):
    current_site = get_current_site(request)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TweetForm(request.POST)
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, 'Tweet posted successfully.')            
                return redirect(reverse('twitter:home'))
    tweets = Tweets.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'tweets': tweets, 'site':current_site})

@login_required
def like_tweet(request, pk):
    tweet = get_object_or_404(Tweets, pk=pk)
    user = request.user.id
    if tweet.likes.filter(id=user):
        tweet.likes.remove(request.user)
        tweet.save()
    else:
        tweet.likes.add(request.user)
    tweet.save()
    # using HTTP_REFERER header to redirect to the same page
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def profile(request, pk):
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

def share_tweet(request, pk):
    tweet = get_object_or_404(Tweets, pk=pk)
    if tweet:
        return render(request, 'twitter/share_tweet.html', {'tweet': tweet})
    messages.error(request, 'Tweet not found.')
    return redirect(reverse('twitter:home'))