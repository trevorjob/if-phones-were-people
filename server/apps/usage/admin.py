from django.contrib import admin
from .models import UsageData, AppUsage, UsagePattern, UsageGoal


@admin.register(UsageData)
class UsageDataAdmin(admin.ModelAdmin):
    list_display = ['device', 'date', 'total_screen_time', 'unlock_count', 'synced_at']
    list_filter = ['date', 'synced_at', 'is_weekend']
    search_fields = ['device__name', 'device__user__username']
    readonly_fields = ['synced_at', 'updated_at']
    date_hierarchy = 'date'


@admin.register(AppUsage)
class AppUsageAdmin(admin.ModelAdmin):
    list_display = ['device_app', 'date', 'time_spent_minutes', 'launch_count']
    list_filter = ['date']
    search_fields = ['device_app__app__name', 'device_app__device__user__username']
    date_hierarchy = 'date'


@admin.register(UsagePattern)
class UsagePatternAdmin(admin.ModelAdmin):
    list_display = ['user', 'pattern_type', 'strength', 'confidence_score', 'is_active', 'start_date', 'end_date']
    list_filter = ['pattern_type', 'strength', 'is_active', 'start_date']
    search_fields = ['user__username', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'device', 'pattern_type', 'description')
        }),
        ('Analysis', {
            'fields': ('strength', 'confidence_score', 'pattern_data')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'frequency')
        }),
        ('Impact', {
            'fields': ('impact_on_productivity', 'impact_on_wellness')
        }),
        ('Status', {
            'fields': ('is_active', 'user_acknowledged')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UsageGoal)
class UsageGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal_type', 'target_minutes_daily', 'current_streak', 'is_active', 'start_date', 'end_date']
    list_filter = ['goal_type', 'is_active', 'start_date']
    search_fields = ['user__username', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'device', 'app', 'goal_type', 'notes')
        }),
        ('Target', {
            'fields': ('target_minutes_daily', 'target_sessions_daily', 'cutoff_time')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'duration_days')
        }),
        ('Progress', {
            'fields': ('current_streak', 'best_streak', 'total_successful_days', 'completion_percentage')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

