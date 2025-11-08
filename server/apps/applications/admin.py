from django.contrib import admin
from .models import AppCategory, App, DeviceApp, AppRelationship


@admin.register(AppCategory)
class AppCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ['name', 'bundle_id', 'category', 'default_personality', 'icon']
    list_filter = ['category', 'default_personality']
    search_fields = ['name', 'bundle_id', 'description']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'bundle_id', 'category', 'description', 'icon')
        }),
        ('Personality', {
            'fields': ('default_personality', 'personality_description')
        }),
    )


@admin.register(DeviceApp)
class DeviceAppAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'device', 'app', 'is_installed', 'is_favorite', 'install_date', 'last_used']
    list_filter = ['is_installed', 'is_favorite', 'install_date', 'last_used']
    search_fields = ['custom_name', 'device__name', 'app__name', 'device__user__username']
    readonly_fields = ['install_date', 'last_used']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('device', 'app', 'custom_name', 'is_installed')
        }),
        ('Personality', {
            'fields': ('custom_personality', 'personality_override')
        }),
        ('Status', {
            'fields': ('is_favorite', 'install_date', 'last_used')
        }),
    )


@admin.register(AppRelationship)
class AppRelationshipAdmin(admin.ModelAdmin):
    list_display = ['app1', 'app2', 'relationship_type', 'strength']
    list_filter = ['relationship_type']
    search_fields = ['app1__name', 'app2__name']

