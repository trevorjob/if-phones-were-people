from django.contrib import admin
from .models import AppCategory, App, DeviceApp, AppRelationship


@admin.register(AppCategory)
class AppCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ['name', 'bundle_id', 'category', 'default_personality', 'icon_url']
    list_filter = ['category', 'default_personality', 'is_social_media', 'is_productivity']
    search_fields = ['name', 'bundle_id', 'personality_description']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'bundle_id', 'category', 'icon_url', 'primary_color')
        }),
        ('Personality', {
            'fields': ('default_personality', 'personality_description')
        }),
        ('Characteristics', {
            'fields': ('is_social_media', 'is_productivity', 'is_entertainment', 'is_work_related', 'is_game')
        }),
    )


@admin.register(DeviceApp)
class DeviceAppAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'device', 'app', 'is_active', 'is_favorite', 'first_installed', 'last_used']
    list_filter = ['is_active', 'is_favorite', 'is_hidden', 'conversation_participation']
    search_fields = ['custom_name', 'device__name', 'app__name', 'device__user__username']
    readonly_fields = ['first_installed', 'last_used', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('device', 'app', 'custom_name', 'version')
        }),
        ('Personality', {
            'fields': ('personality_override', 'custom_personality_notes')
        }),
        ('Status', {
            'fields': ('is_active', 'is_favorite', 'is_hidden', 'first_installed', 'last_used')
        }),
        ('Conversation Settings', {
            'fields': ('conversation_participation', 'conversation_frequency')
        }),
    )


@admin.register(AppRelationship)
class AppRelationshipAdmin(admin.ModelAdmin):
    list_display = ['app_a', 'app_b', 'relationship_type', 'same_device', 'interactions_count']
    list_filter = ['relationship_type', 'same_device', 'user_created']
    search_fields = ['app_a__app__name', 'app_b__app__name', 'notes']

