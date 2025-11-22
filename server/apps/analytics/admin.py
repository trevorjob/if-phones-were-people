from django.contrib import admin
from .models import UserStats, TrendAnalysis


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'total_screen_time_all_devices', 'total_pickups_all_devices', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user', 'date')
        }),
        ('Totals', {
            'fields': ('total_screen_time_all_devices', 'total_pickups_all_devices')
        }),
        ('Category Breakdowns', {
            'fields': ('social_media_time', 'productivity_time', 'entertainment_time', 'communication_time')
        }),
        ('Rankings', {
            'fields': ('screen_time_rank', 'productivity_rank')
        }),
        ('Insights', {
            'fields': ('weekly_trend', 'notable_patterns')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(TrendAnalysis)
class TrendAnalysisAdmin(admin.ModelAdmin):
    list_display = ['user', 'period_type', 'start_date', 'end_date', 'created_at']
    list_filter = ['period_type', 'start_date', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'period_type', 'start_date', 'end_date')
        }),
        ('Trends', {
            'fields': ('screen_time_trend', 'app_usage_trends', 'category_trends')
        }),
        ('Insights', {
            'fields': ('key_insights', 'recommendations')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

