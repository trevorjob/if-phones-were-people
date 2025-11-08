from django.contrib import admin
from .models import DeviceType, PersonalityTrait, Device, DeviceRelationship


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon']
    search_fields = ['name', 'description']


@admin.register(PersonalityTrait)
class PersonalityTraitAdmin(admin.ModelAdmin):
    list_display = ['trait_name', 'trait_code', 'description']
    search_fields = ['trait_name', 'trait_code', 'description']
    list_filter = ['trait_code']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'platform', 'device_type', 'personality_type', 'is_primary', 'is_active', 'last_used']
    list_filter = ['platform', 'device_type', 'personality_type', 'is_primary', 'is_active', 'created_at']
    search_fields = ['name', 'user__username', 'device_id']
    readonly_fields = ['device_id', 'created_at', 'updated_at', 'last_used']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'device_id', 'platform', 'device_type')
        }),
        ('Personality', {
            'fields': ('personality_type', 'personality_description', 'custom_personality')
        }),
        ('Status', {
            'fields': ('is_primary', 'is_active', 'last_used')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DeviceRelationship)
class DeviceRelationshipAdmin(admin.ModelAdmin):
    list_display = ['device1', 'device2', 'relationship_type', 'strength', 'created_at']
    list_filter = ['relationship_type', 'created_at']
    search_fields = ['device1__name', 'device2__name']
    readonly_fields = ['created_at']

