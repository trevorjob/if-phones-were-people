from django.contrib import admin
from .models import FriendConnection, TemporaryDeviceConnection, Challenge


@admin.register(FriendConnection)
class FriendConnectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend_user', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'friend_user__username']
    readonly_fields = ['created_at']


@admin.register(TemporaryDeviceConnection)
class TemporaryDeviceConnectionAdmin(admin.ModelAdmin):
    list_display = ['visitor_device', 'host_user', 'visitor_user', 'connection_name', 'is_active', 'expires_at']
    list_filter = ['is_active', 'created_at', 'expires_at']
    search_fields = ['visitor_device__name', 'host_user__username', 'visitor_user__username', 'connection_name']
    readonly_fields = ['created_at', 'activated_at']


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'challenge_type', 'creator', 'start_date', 'end_date', 'is_active']
    list_filter = ['challenge_type', 'is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description', 'creator__username']
    readonly_fields = ['created_at']
    filter_horizontal = ['participants']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'challenge_type', 'creator')
        }),
        ('Participants', {
            'fields': ('participants',)
        }),
        ('Target', {
            'fields': ('target_metric', 'target_value')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'duration_days', 'is_active')
        }),
        ('Results', {
            'fields': ('winner',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

