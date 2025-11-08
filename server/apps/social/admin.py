from django.contrib import admin
from .models import FriendConnection, TemporaryDeviceConnection, Challenge, ChallengeParticipant


@admin.register(FriendConnection)
class FriendConnectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'friend__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TemporaryDeviceConnection)
class TemporaryDeviceConnectionAdmin(admin.ModelAdmin):
    list_display = ['device', 'temporary_device', 'connection_type', 'duration_minutes', 'connected_at', 'expires_at']
    list_filter = ['connection_type', 'connected_at', 'expires_at']
    search_fields = ['device__name', 'temporary_device__name']
    readonly_fields = ['connected_at']


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'challenge_type', 'creator', 'start_date', 'end_date', 'is_active']
    list_filter = ['challenge_type', 'is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description', 'creator__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'challenge_type', 'creator')
        }),
        ('Target', {
            'fields': ('target_value', 'target_apps')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChallengeParticipant)
class ChallengeParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'status', 'current_value', 'joined_at']
    list_filter = ['status', 'joined_at']
    search_fields = ['user__username', 'challenge__title']
    readonly_fields = ['joined_at', 'completed_at']

