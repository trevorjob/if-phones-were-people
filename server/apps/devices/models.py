# devices/models.py
from django.db import models
from django.contrib.auth import get_user_model
import uuid
import json

User = get_user_model()

class DeviceType(models.Model):
    """Predefined device types with default personalities"""
    name = models.CharField(max_length=30, unique=True)
    default_personality = models.CharField(max_length=30)
    icon = models.CharField(max_length=50, blank=True)  # CSS class or emoji
    platform_category = models.CharField(
        max_length=20,
        choices=[
            ('mobile', 'Mobile'),
            ('desktop', 'Desktop'),
            ('tablet', 'Tablet'),
            ('wearable', 'Wearable'),
            ('other', 'Other')
        ]
    )
    
    def __str__(self):
        return self.name

class PersonalityTrait(models.Model):
    """Individual personality traits that can be combined"""
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    speech_patterns = models.JSONField(default=dict, help_text="JSON object with speech characteristics")
    
    # Trait categories
    category = models.CharField(
        max_length=20,
        choices=[
            ('temperament', 'Temperament'),
            ('humor', 'Humor Style'),
            ('communication', 'Communication'),
            ('attitude', 'Attitude'),
            ('quirks', 'Quirks')
        ]
    )
    
    # Compatibility with other traits
    compatible_traits = models.ManyToManyField('self', blank=True, symmetrical=False)
    conflicting_traits = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='conflicts_with')
    
    def __str__(self):
        return self.name

class Device(models.Model):
    """User's devices with personalities"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    
    # Basic device info
    name = models.CharField(max_length=50)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    platform = models.CharField(
        max_length=20,
        choices=[
            ('ios', 'iOS'),
            ('android', 'Android'),
            ('windows', 'Windows'),
            ('macos', 'macOS'),
            ('linux', 'Linux'),
            ('web', 'Web Browser'),
            ('other', 'Other')
        ]
    )
    
    # Device identification for data collection
    device_identifier = models.CharField(max_length=100, blank=True)  # UUID from device
    model_name = models.CharField(max_length=50, blank=True)  # iPhone 15 Pro, MacBook Air, etc.
    os_version = models.CharField(max_length=20, blank=True)
    
    # Personality system
    personality_type = models.CharField(
        max_length=30,
        choices=[
            ('snarky', 'Snarky'),
            ('logical', 'Logical'),
            ('chaotic', 'Chaotic'),
            ('supportive', 'Supportive'),
            ('dramatic', 'Dramatic'),
            ('minimalist', 'Minimalist'),
            ('workaholic', 'Workaholic'),
            ('social', 'Social Butterfly'),
            ('creative', 'Creative'),
            ('anxious', 'Anxious'),
            ('chill', 'Chill'),
            ('competitive', 'Competitive')
        ]
    )
    
    personality_traits = models.ManyToManyField(PersonalityTrait, blank=True)
    custom_personality_notes = models.TextField(blank=True)
    
    # Status and settings
    is_active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)  # User's main device
    data_collection_enabled = models.BooleanField(default=True)
    
    # Last seen data
    last_sync = models.DateTimeField(null=True, blank=True)
    last_usage = models.DateTimeField(null=True, blank=True)
    battery_level = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'device_identifier']
        ordering = ['-is_primary', '-last_usage', 'name']
    
    def __str__(self):
        return f"{self.user.username}'s {self.name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one primary device per user
        if self.is_primary:
            Device.objects.filter(user=self.user, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
    
    @property
    def personality_description(self):
        """Generate a description based on personality type and traits"""
        base_descriptions = {
            'snarky': "Always has a witty comeback and isn't afraid to call out digital habits",
            'logical': "Approaches everything with data and reason, loves efficiency",
            'chaotic': "Unpredictable and spontaneous, embraces digital chaos",
            'supportive': "Always encouraging and helpful, your digital cheerleader",
            'dramatic': "Everything is a big deal, loves to exaggerate usage patterns",
            'minimalist': "Prefers simplicity, judges cluttered digital lives",
            'workaholic': "All about productivity and getting things done",
            'social': "Loves connections, social media, and sharing experiences",
            'creative': "Inspires artistic pursuits and creative projects",
            'anxious': "Worries about screen time, security, and digital wellness",
            'chill': "Laid back about everything, goes with the flow",
            'competitive': "Turns everything into a game or competition"
        }
        return base_descriptions.get(self.personality_type, "A unique digital personality")
    
    @property
    def total_apps(self):
        return self.device_apps.count()
    
    @property
    def active_apps(self):
        return self.device_apps.filter(is_active=True)

class DeviceRelationship(models.Model):
    """Relationships between user's devices"""
    device_a = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='relationships_as_a')
    device_b = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='relationships_as_b')
    
    relationship_type = models.CharField(
        max_length=30,
        choices=[
            ('rivals', 'Rivals'),
            ('best_friends', 'Best Friends'),
            ('work_partners', 'Work Partners'),
            ('siblings', 'Like Siblings'),
            ('mentor_student', 'Mentor & Student'),
            ('frenemies', 'Frenemies'),
            ('ignored', 'Barely Acknowledge Each Other')
        ]
    )
    
    intensity = models.IntegerField(default=5, help_text="Relationship intensity from 1-10")
    notes = models.TextField(blank=True)
    
    # Dynamic relationship data
    interactions_count = models.IntegerField(default=0)
    last_interaction = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['device_a', 'device_b']
    
    def __str__(self):
        return f"{self.device_a.name} & {self.device_b.name}: {self.relationship_type}"