from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_device_type', 'digital_wellness_goal', 'created_at']
    list_filter = ['favorite_device_type', 'digital_wellness_goal', 'created_at']
    search_fields = ['user__username', 'user__email', 'friend_code']
    readonly_fields = ['created_at', 'updated_at', 'friend_code']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Preferences', {
            'fields': ('favorite_device_type', 'digital_wellness_goal')
        }),
        ('Social Settings', {
            'fields': ('friend_code', 'allow_device_invites', 'auto_accept_close_friends')
        }),
        ('Notifications', {
            'fields': ('daily_summary_enabled', 'conversation_notifications', 'weekly_insights', 'friend_activity_notifications')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Extend the default User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']


# Register UserAdmin
admin.site.register(User, CustomUserAdmin)

