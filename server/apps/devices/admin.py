from django.contrib import admin
from .models import DeviceType, PersonalityTrait, Device, DeviceRelationship


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'default_personality', 'platform_category', 'icon']
    search_fields = ['name', 'default_personality']
    list_filter = ['platform_category']


@admin.register(PersonalityTrait)
class PersonalityTraitAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description']
    search_fields = ['name', 'description']
    list_filter = ['category']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'platform', 'device_type', 'personality_type', 'is_primary', 'is_active', 'last_usage']
    list_filter = ['platform', 'device_type', 'personality_type', 'is_primary', 'is_active', 'created_at']
    search_fields = ['name', 'user__username', 'device_identifier']
    readonly_fields = ['created_at', 'updated_at', 'last_usage']    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'device_identifier', 'platform', 'device_type', 'model_name', 'os_version')
        }),
        ('Personality', {
            'fields': ('personality_type', 'personality_traits', 'custom_personality_notes')
        }),
        ('Status', {
            'fields': ('is_primary', 'is_active', 'data_collection_enabled', 'last_sync', 'last_usage', 'battery_level')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DeviceRelationship)
class DeviceRelationshipAdmin(admin.ModelAdmin):
    list_display = ['device_a', 'device_b', 'relationship_type', 'intensity', 'created_at']
    list_filter = ['relationship_type', 'created_at']
    search_fields = ['device_a__name', 'device_b__name']
    readonly_fields = ['created_at', 'updated_at']

