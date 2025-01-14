from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from twitter.models import Profile, Tweets
from .forms import FollowForm, TweetForm, UserUpdateForm, UserProfileUpdateForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
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
    if search := request.GET.get('search'):
        tweets = Tweets.objects.filter(tweet__contains = search).order_by('-created_at')
    return render(request, 'home.html', {'tweets': tweets, 'site':current_site})

@login_required
def profile(request, pk):
    current_site = get_current_site(request)
    profile = get_object_or_404(Profile, user__pk=pk)
    tweets = Tweets.objects.filter(user=profile.user).order_by('-created_at')
    return render(request, 'twitter/profile.html', {'profile': profile, 'tweets': tweets, 'site':current_site})

@login_required
def profiles(request):
    profiles = Profile.objects.exclude(user=request.user.id)
    if search := request.GET.get('search'):
        profiles = Profile.objects.filter(Q(user__username__contains=search) | Q(user__first_name__contains=search) |Q(user__last_name__contains=search) | Q(user__email__contains=search))
    return render(request, 'twitter/profiles.html', {'profiles': profiles})

@login_required
def follow_unfollow(request, pk): # this view is used to follow and unfollow users
    profile = get_object_or_404(Profile, user__pk=pk)
    current_user_profile = request.user.profile
    # if user already follows the profile, unfollow it
    if current_user_profile.follows.filter(user__pk=pk):
        current_user_profile.follows.remove(profile)
        current_user_profile.save()
        messages.success(request, f'You have unfollowed {profile.user.username}.')
    else:
        current_user_profile.follows.add(profile)
        current_user_profile.save()
        messages.success(request, f'You are now following {profile.user.username}.')
    return redirect(request.META.get('HTTP_REFERER'))

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

def share_tweet(request, pk):
    tweet = get_object_or_404(Tweets, pk=pk)
    current_site = get_current_site(request)

    if tweet:
        return render(request, 'twitter/share_tweet.html', {'tweet': tweet, 'site':current_site})
    messages.error(request, 'Tweet not found.')
    return redirect(reverse('twitter:home'))
@login_required
def delete_tweet(request, pk):
    tweet = get_object_or_404(Tweets, pk=pk)
    if tweet:
        if request.user.id == tweet.user.id:
            tweet.delete()
            messages.success(request, 'Tweet successfuly deleted.')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'You not own this tweet.')
            return redirect(reverse('twitter:home'))
@login_required
def edit_tweet(request, pk):
    tweet = get_object_or_404(Tweets, pk=pk)
    form = TweetForm()
    if request.user.pk == tweet.user.pk:
        if request.method == "POST":
            form = TweetForm(request.POST or None, instance=tweet)
            if form.is_valid():
                new_tweet = form.save(commit=False)
                new_tweet.user = request.user
                new_tweet.save()
                messages.success(request, "You'r Tweet has Updated!")
                return redirect(reverse("twitter:home"))
            else:
                messages.error(request, "Error is occure during edit Tweet ...")
                return redirect(request.META.get('HTTP_REFERER'))
                
    return render(request, 'twitter/edit_tweet.html', {"tweet":tweet, "form":form})
