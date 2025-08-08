from django.contrib import admin
from .models import UserProfile, Follow, UserActivity

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'position', 'is_contributor', 'created_at')
    list_filter = ('is_contributor', 'industry', 'created_at')
    search_fields = ('user__username', 'user__email', 'company', 'position')
    date_hierarchy = 'created_at'

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')
    date_hierarchy = 'created_at'

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'description', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__username', 'description')
    date_hierarchy = 'created_at' 