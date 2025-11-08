from django.contrib import admin
from .models import UserStats, TrendAnalysis


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_screen_time', 'avg_daily_screen_time', 'wellness_score', 'current_streak', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Screen Time', {
            'fields': ('total_screen_time', 'avg_daily_screen_time', 'peak_usage_day', 'peak_usage_amount')
        }),
        ('Activity', {
            'fields': ('total_unlocks', 'avg_daily_unlocks', 'active_days', 'current_streak', 'longest_streak')
        }),
        ('Apps & Devices', {
            'fields': ('most_used_app', 'most_used_app_time', 'most_productive_app', 'favorite_device')
        }),
        ('Social & Goals', {
            'fields': ('friends_count', 'goals_achieved', 'challenges_completed', 'achievements_earned')
        }),
        ('Conversations', {
            'fields': ('total_conversations', 'conversations_read')
        }),
        ('Patterns & Wellness', {
            'fields': ('active_patterns', 'wellness_score')
        }),
        ('Comparisons', {
            'fields': ('week_comparison', 'month_comparison')
        }),
        ('Timestamp', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(TrendAnalysis)
class TrendAnalysisAdmin(admin.ModelAdmin):
    list_display = ['trend_type', 'period', 'date', 'created_at']
    list_filter = ['trend_type', 'period', 'date', 'created_at']
    search_fields = ['trend_type']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('trend_type', 'period', 'date')
        }),
        ('Data', {
            'fields': ('data',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

