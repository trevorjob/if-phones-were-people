from django.contrib import admin
from .models import UsageData, AppUsageData, UsagePattern, UsageGoal


@admin.register(UsageData)
class UsageDataAdmin(admin.ModelAdmin):
    list_display = ['device', 'date', 'total_screen_time', 'unlock_count', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['device__name', 'device__user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'


@admin.register(AppUsageData)
class AppUsageDataAdmin(admin.ModelAdmin):
    list_display = ['device_app', 'usage_data', 'time_spent', 'launch_count']
    list_filter = ['usage_data__date']
    search_fields = ['device_app__app__name', 'device_app__device__user__username']
    date_hierarchy = 'usage_data__date'


@admin.register(UsagePattern)
class UsagePatternAdmin(admin.ModelAdmin):
    list_display = ['user', 'pattern_type', 'severity', 'confidence', 'resolved', 'first_detected', 'last_detected']
    list_filter = ['pattern_type', 'severity', 'resolved', 'first_detected']
    search_fields = ['user__username', 'description']
    readonly_fields = ['first_detected', 'last_detected']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'pattern_type', 'description')
        }),
        ('Analysis', {
            'fields': ('severity', 'confidence', 'metadata')
        }),
        ('Status', {
            'fields': ('resolved', 'resolution_notes')
        }),
        ('Timestamps', {
            'fields': ('first_detected', 'last_detected'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UsageGoal)
class UsageGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal_type', 'target_value', 'current_value', 'status', 'start_date', 'end_date']
    list_filter = ['goal_type', 'status', 'start_date']
    search_fields = ['user__username', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'goal_type', 'description')
        }),
        ('Target', {
            'fields': ('target_value', 'current_value', 'target_apps')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

