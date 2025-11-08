# social/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class FriendConnection(models.Model):
    """Friend relationships between users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_connections')
    friend_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of_connections')
    
    is_active = models.BooleanField(default=True)
    can_compare_stats = models.BooleanField(default=True)
    can_see_conversations = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'friend_user']
    
    def __str__(self):
        return f"{self.user.username} <-> {self.friend_user.username}"

class TemporaryDeviceConnection(models.Model):
    """Temporary connections for visiting friends' devices"""
    host_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_connections')
    visitor_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visitor_connections')
    visitor_device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, related_name='temporary_connections')
    
    # Connection details
    connection_name = models.CharField(max_length=100)  # "Weekend Hackathon", "Movie Night"
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    # Permissions
    can_participate_in_conversations = models.BooleanField(default=True)
    can_see_usage_stats = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)
    activated_at = models.DateTimeField(null=True, blank=True)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"{self.visitor_device.name} visiting {self.host_user.username}"

class Challenge(models.Model):
    """Social challenges between friends"""
    CHALLENGE_TYPES = [
        ('screen_time_reduction', 'Screen Time Reduction'),
        ('productivity_boost', 'Productivity Boost'),
        ('social_media_detox', 'Social Media Detox'),
        ('early_bird', 'Early Bird Challenge'),
        ('night_owl_recovery', 'Night Owl Recovery'),
    ]
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges')
    participants = models.ManyToManyField(User, related_name='challenges')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(max_length=30, choices=CHALLENGE_TYPES)
    
    # Duration
    start_date = models.DateField()
    end_date = models.DateField()
    duration_days = models.IntegerField()
    
    # Challenge parameters
    target_metric = models.CharField(max_length=50)  # 'total_screen_time', 'social_media_time', etc.
    target_value = models.FloatField()  # Target value for the metric
    
    # Status
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_challenges')
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.title} ({self.creator.username})"
