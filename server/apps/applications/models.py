# apps/models.py
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class AppCategory(models.Model):
    """Categories for organizing apps"""
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#6B7280')  # Hex color
    
    # Default personality traits for this category
    default_personality_traits = models.JSONField(default=list)
    
    class Meta:
        verbose_name_plural = "App Categories"
    
    def __str__(self):
        return self.name

class App(models.Model):
    """Master app registry with default personalities"""
    name = models.CharField(max_length=100)
    bundle_id = models.CharField(max_length=200, unique=True)  # com.apple.safari, etc.
    category = models.ForeignKey(AppCategory, on_delete=models.CASCADE, related_name='apps')
    
    # App identification across platforms
    ios_bundle_id = models.CharField(max_length=200, blank=True)
    android_package = models.CharField(max_length=200, blank=True)
    windows_exe = models.CharField(max_length=200, blank=True)
    mac_bundle_id = models.CharField(max_length=200, blank=True)
    
    # Visual identity
    icon_url = models.URLField(blank=True)
    primary_color = models.CharField(max_length=7, blank=True)
    
    # Default personality
    default_personality = models.CharField(
        max_length=30,
        choices=[
            ('attention_seeking', 'Attention Seeking'),
            ('workaholic', 'Workaholic'),
            ('chill', 'Chill'),
            ('chaotic', 'Chaotic'),
            ('creative', 'Creative'),
            ('social', 'Social'),
            ('analytical', 'Analytical'),
            ('entertaining', 'Entertaining'),
            ('productive', 'Productive'),
            ('addictive', 'Addictive'),
            ('helpful', 'Helpful'),
            ('dramatic', 'Dramatic'),
            ('competitive', 'Competitive'),
            ('educational', 'Educational'),
            ('gossip', 'Gossip'),
            ('minimalist', 'Minimalist')
        ]
    )
    
    personality_description = models.TextField(blank=True)
    
    # App characteristics
    is_social_media = models.BooleanField(default=False)
    is_productivity = models.BooleanField(default=False)
    is_entertainment = models.BooleanField(default=False)
    is_work_related = models.BooleanField(default=False)
    is_game = models.BooleanField(default=False)
    
    # Common usage patterns
    typical_session_length = models.IntegerField(null=True, blank=True, help_text="Typical session in minutes")
    addictive_potential = models.IntegerField(default=5, help_text="Addictive potential 1-10")
    productivity_score = models.IntegerField(default=5, help_text="Productivity score 1-10")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def total_users(self):
        return self.device_apps.values('device__user').distinct().count()

class DeviceApp(models.Model):
    """Apps installed on specific devices with custom personalities"""
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, related_name='device_apps')
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='device_apps')
    
    # Custom naming and personality
    custom_name = models.CharField(max_length=100, blank=True)
    personality_override = models.CharField(
        max_length=30,
        choices=[
            ('attention_seeking', 'Attention Seeking'),
            ('workaholic', 'Workaholic'),
            ('chill', 'Chill'),
            ('chaotic', 'Chaotic'),
            ('creative', 'Creative'),
            ('social', 'Social'),
            ('analytical', 'Analytical'),
            ('entertaining', 'Entertaining'),
            ('productive', 'Productive'),
            ('addictive', 'Addictive'),
            ('helpful', 'Helpful'),
            ('dramatic', 'Dramatic'),
            ('competitive', 'Competitive'),
            ('educational', 'Educational'),
            ('gossip', 'Gossip'),
            ('minimalist', 'Minimalist')
        ],
        blank=True
    )
    
    custom_personality_notes = models.TextField(blank=True)
    
    # App status on device
    is_active = models.BooleanField(default=True)
    is_favorite = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)  # Hide from conversations
    
    # Installation and usage tracking
    first_installed = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    version = models.CharField(max_length=20, blank=True)
    
    # Conversation participation
    conversation_participation = models.BooleanField(default=True)
    conversation_frequency = models.CharField(
        max_length=20,
        choices=[
            ('always', 'Always Participate'),
            ('significant', 'Only Significant Usage'),
            ('mentioned', 'Only When Mentioned'),
            ('never', 'Never Participate')
        ],
        default='significant'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['device', 'app']
        ordering = ['-is_favorite', '-last_used', 'app__name']
    
    def __str__(self):
        name = self.custom_name or self.app.name
        return f"{name} on {self.device.name}"
    
    @property
    def display_name(self):
        return self.custom_name or self.app.name
    
    @property
    def effective_personality(self):
        return self.personality_override or self.app.default_personality
    
    @property
    def personality_description(self):
        if self.custom_personality_notes:
            return self.custom_personality_notes
        return self.app.personality_description

class AppRelationship(models.Model):
    """Relationships between apps (can be on same or different devices)"""
    app_a = models.ForeignKey(DeviceApp, on_delete=models.CASCADE, related_name='relationships_as_a')
    app_b = models.ForeignKey(DeviceApp, on_delete=models.CASCADE, related_name='relationships_as_b')
    
    relationship_type = models.CharField(
        max_length=30,
        choices=[
            ('rivals', 'Rivals'),
            ('best_friends', 'Best Friends'),
            ('work_partners', 'Work Partners'),
            ('frenemies', 'Frenemies'),
            ('mentor_student', 'Mentor & Student'),
            ('gossip_buddies', 'Gossip Buddies'),
            ('competitors', 'Competitors'),
            ('enablers', 'Enablers'),  # Help each other waste time
            ('productivity_team', 'Productivity Team'),
            ('ignore_each_other', 'Ignore Each Other')
        ]
    )
    
    # Relationship context
    same_device = models.BooleanField(default=True)
    user_created = models.BooleanField(default=False)  # Did user manually set this?
    
    # Dynamic relationship tracking
    interactions_count = models.IntegerField(default=0)
    co_usage_frequency = models.FloatField(default=0.0)  # How often used together
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['app_a', 'app_b']
    
    def __str__(self):
        return f"{self.app_a.display_name} & {self.app_b.display_name}: {self.relationship_type}"

class AppPersonalityPreset(models.Model):
    """Predefined personality presets for apps"""
    name = models.CharField(max_length=50)
    description = models.TextField()
    
    # Personality characteristics
    speech_patterns = models.JSONField(default=dict)
    conversation_style = models.CharField(
        max_length=30,
        choices=[
            ('talkative', 'Very Talkative'),
            ('moderate', 'Moderate'),
            ('quiet', 'Quiet'),
            ('only_important', 'Only Important Topics')
        ],
        default='moderate'
    )
    
    # Common phrases and reactions
    common_phrases = models.JSONField(default=list)
    reaction_triggers = models.JSONField(default=dict)  # What triggers responses
    
    # App types this preset works well with
    suitable_for_categories = models.ManyToManyField(AppCategory, blank=True)
    
    def __str__(self):
        return self.name