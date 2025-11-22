# usage/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()

class UsageData(models.Model):
    """Daily usage data for devices"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, related_name='usage_data')
    date = models.DateField()
    
    # Overall device usage
    total_screen_time = models.IntegerField(default=0, help_text="Total screen time in minutes")
    unlock_count = models.IntegerField(default=0)
    pickup_count = models.IntegerField(default=0)
    notification_count = models.IntegerField(default=0)
    
    # Time patterns
    first_pickup_time = models.TimeField(null=True, blank=True)
    last_usage_time = models.TimeField(null=True, blank=True)
    longest_session_minutes = models.IntegerField(default=0)
    average_session_minutes = models.FloatField(default=0.0)
    
    # Usage distribution by hour (JSON array of 24 values)
    hourly_usage = models.JSONField(default=list, help_text="Array of 24 hourly usage values in minutes")
    
    # Battery and device health
    battery_start = models.IntegerField(null=True, blank=True)
    battery_end = models.IntegerField(null=True, blank=True)
    charging_time_minutes = models.IntegerField(default=0)
    
    # Usage context
    weekday = models.IntegerField()  # 0=Monday, 6=Sunday
    is_weekend = models.BooleanField(default=False)
    is_holiday = models.BooleanField(default=False)
    
    # Data quality
    data_completeness = models.FloatField(default=1.0, help_text="0.0 to 1.0, how complete is this data")
    collection_method = models.CharField(
        max_length=20,
        choices=[
            ('ios_shortcuts', 'iOS Shortcuts'),
            ('android_service', 'Android Background Service'),
            ('manual_entry', 'Manual Entry'),
            ('estimated', 'Estimated Data'),
            ('api_sync', 'Third-party API Sync')
        ]
    )
    
    # Metadata
    synced_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['device', 'date']
        ordering = ['-date', 'device']
    
    def __str__(self):
        return f"{self.device.name} - {self.date} ({self.total_screen_time}min)"
    
    @property
    def screen_time_hours(self):
        return round(self.total_screen_time / 60, 2)
    
    @property
    def is_heavy_usage_day(self):
        return self.total_screen_time > 480  # 8+ hours
    
    @property
    def is_light_usage_day(self):
        return self.total_screen_time < 60  # Less than 1 hour
    
    @property
    def usage_intensity(self):
        """Calculate usage intensity based on screen time and patterns"""
        if self.total_screen_time == 0:
            return 'none'
        elif self.total_screen_time < 60:
            return 'light'
        elif self.total_screen_time < 240:
            return 'moderate'
        elif self.total_screen_time < 480:
            return 'heavy'
        else:
            return 'extreme'

class AppUsage(models.Model):
    """Daily app usage data"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_app = models.ForeignKey('applications.DeviceApp', on_delete=models.CASCADE, related_name='usage_data')
    date = models.DateField()
    
    # Basic usage metrics
    time_spent_minutes = models.IntegerField(default=0)
    launch_count = models.IntegerField(default=0)
    notification_count = models.IntegerField(default=0)
    background_time_minutes = models.IntegerField(default=0)
    
    # Session information
    session_count = models.IntegerField(default=0)
    longest_session_minutes = models.IntegerField(default=0)
    average_session_minutes = models.FloatField(default=0.0)
    
    # Time patterns
    first_launch_time = models.TimeField(null=True, blank=True)
    last_usage_time = models.TimeField(null=True, blank=True)
    peak_usage_hour = models.IntegerField(null=True, blank=True)  # 0-23
    
    # Usage distribution by hour
    hourly_usage = models.JSONField(default=list, help_text="Array of 24 hourly usage values in minutes")
    
    # App-specific metrics
    scrolled_distance = models.IntegerField(null=True, blank=True, help_text="Distance scrolled in pixels")
    items_viewed = models.IntegerField(null=True, blank=True)
    actions_performed = models.IntegerField(null=True, blank=True)
    
    # Context
    usage_context = models.JSONField(default=dict, help_text="Additional context like location, other apps used")
    
    # Data quality
    data_completeness = models.FloatField(default=1.0)
    estimated = models.BooleanField(default=False)
    
    synced_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['device_app', 'date']
        ordering = ['-date', '-time_spent_minutes']
    
    def __str__(self):
        return f"{self.device_app.display_name} - {self.date} ({self.time_spent_minutes}min)"
    
    @property
    def time_spent_hours(self):
        return round(self.time_spent_minutes / 60, 2)
    
    @property
    def is_binge_session(self):
        return self.longest_session_minutes > 120  # 2+ hours
    
    @property
    def usage_intensity(self):
        """Categorize app usage intensity"""
        if self.time_spent_minutes == 0:
            return 'none'
        elif self.time_spent_minutes < 15:
            return 'minimal'
        elif self.time_spent_minutes < 60:
            return 'light'
        elif self.time_spent_minutes < 180:
            return 'moderate'
        elif self.time_spent_minutes < 360:
            return 'heavy'
        else:
            return 'extreme'

class UsagePattern(models.Model):
    """Detected usage patterns and insights"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usage_patterns')
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, null=True, blank=True)
    
    pattern_type = models.CharField(
        max_length=30,
        choices=[
            ('binge_usage', 'Binge Usage'),
            ('night_owl', 'Night Owl'),
            ('morning_person', 'Morning Person'),
            ('weekend_warrior', 'Weekend Warrior'),
            ('distracted', 'Distracted'),
            ('doom_scrolling', 'Doom Scrolling'),
            ('phantom_vibration', 'Phantom Vibration'),
            ('app_switching', 'App Switching'),
            ('notification_addiction', 'Notification Addiction')
        ]
    )
    
    # Pattern details
    description = models.TextField()
    confidence_score = models.FloatField(default=0.0, help_text="0.0 to 1.0 confidence in pattern")
    
    # Time context
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Null for ongoing patterns
    days_observed = models.IntegerField(default=1)
      # Pattern data
    pattern_data = models.JSONField(default=dict, help_text="Detailed pattern information")
    apps_involved = models.ManyToManyField('applications.DeviceApp', blank=True)
    
    # Pattern strength and frequency
    frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekdays', 'Weekdays'),
            ('weekends', 'Weekends'),
            ('weekly', 'Weekly'),
            ('occasional', 'Occasional'),
            ('rare', 'Rare')
        ]
    )
    
    strength = models.CharField(
        max_length=20,
        choices=[
            ('weak', 'Weak Pattern'),
            ('moderate', 'Moderate Pattern'),
            ('strong', 'Strong Pattern'),
            ('very_strong', 'Very Strong Pattern')
        ]
    )
    
    # Impact assessment
    impact_on_productivity = models.IntegerField(default=0, help_text="-5 to +5 scale")
    impact_on_wellness = models.IntegerField(default=0, help_text="-5 to +5 scale")
    
    # Status
    is_active = models.BooleanField(default=True)
    user_acknowledged = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        device_str = f" on {self.device.name}" if self.device else ""
        return f"{self.user.username}: {self.pattern_type}{device_str}"

class UsageGoal(models.Model):
    """User-defined usage goals and tracking"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usage_goals')
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, null=True, blank=True)
    app = models.ForeignKey('applications.DeviceApp', on_delete=models.CASCADE, null=True, blank=True)

    goal_type = models.CharField(
        max_length=30,
        choices=[
            ('reduce_total', 'Reduce Total Screen Time'),
            ('reduce_app', 'Reduce Specific App Usage'),
            ('increase_productive', 'Increase Productive App Usage'),
            ('limit_daily', 'Daily Time Limit'),
            ('digital_sunset', 'Digital Sunset (No Usage After Time)'),
            ('weekend_detox', 'Weekend Digital Detox'),
            ('focus_sessions', 'Focus Sessions'),
            ('app_replacement', 'Replace App with Alternative')
        ]
    )
    
    # Goal parameters
    target_minutes_daily = models.IntegerField(null=True, blank=True)
    target_sessions_daily = models.IntegerField(null=True, blank=True)
    cutoff_time = models.TimeField(null=True, blank=True)
    
    # Goal timeline
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    duration_days = models.IntegerField(null=True, blank=True)
    
    # Progress tracking
    current_streak = models.IntegerField(default=0)
    best_streak = models.IntegerField(default=0)
    total_successful_days = models.IntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    completion_percentage = models.FloatField(default=0.0)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        target = self.device.name if self.device else (self.app.display_name if self.app else "Overall")
        return f"{self.user.username}: {self.goal_type} for {target}"