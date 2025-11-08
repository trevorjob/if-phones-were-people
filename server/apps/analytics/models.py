# ===== ANALYTICS APP =====
# analytics/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class UserStats(models.Model):
    """Aggregated user statistics for comparisons"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stats')
    date = models.DateField()
    
    # Cross-device totals
    total_screen_time_all_devices = models.DurationField(default=timezone.timedelta)
    total_pickups_all_devices = models.IntegerField(default=0)
    
    # Category breakdowns
    social_media_time = models.DurationField(default=timezone.timedelta)
    productivity_time = models.DurationField(default=timezone.timedelta)
    entertainment_time = models.DurationField(default=timezone.timedelta)
    communication_time = models.DurationField(default=timezone.timedelta)
    
    # Rankings (among friends)
    screen_time_rank = models.IntegerField(null=True, blank=True)
    productivity_rank = models.IntegerField(null=True, blank=True)
    
    # Insights
    weekly_trend = models.CharField(max_length=20, blank=True)  # 'increasing', 'decreasing', 'stable'
    notable_patterns = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'date']
        indexes = [
            models.Index(fields=['date', 'total_screen_time_all_devices']),
        ]
    
    def __str__(self):
        return f"{self.user.username} Stats - {self.date}"

class TrendAnalysis(models.Model):
    """Weekly/monthly trend analysis for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trend_analyses')
    period_type = models.CharField(max_length=10, choices=[('weekly', 'Weekly'), ('monthly', 'Monthly')])
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Trend data
    screen_time_trend = models.JSONField(default=dict)  # {date: minutes}
    app_usage_trends = models.JSONField(default=dict)  # {app: trend_data}
    category_trends = models.JSONField(default=dict)
    
    # Insights
    key_insights = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} {self.period_type} trends - {self.start_date}"
