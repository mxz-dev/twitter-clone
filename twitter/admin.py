from django.contrib import admin
from django.contrib.auth.models import Group, User
from twitter.models import Profile, Tweets
# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)
class ProfileInline(admin.StackedInline):
    model  = Profile
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ['user_permissions', 'groups', 'date_joined', 'last_login']
    empty_value_display = "-empty-"
    list_display = ['username', 'email', 'is_staff', 'is_active']
    list_filter = ['is_active']
    search_fields = ["username", "first_name", "last_name", "email"]
    ordering = ['is_active']
    inlines = [ProfileInline]
@admin.register(Tweets)
class TweetsAdmin(admin.ModelAdmin):
    list_display = ['tweet', 'user', 'created_at']
    search_fields = ['tweet', 'user__username']
    list_filter = ['created_at']
    ordering = ['created_at']