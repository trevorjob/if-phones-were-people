# conversations/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
import json

User = get_user_model()

class ConversationTrigger(models.Model):
    """Defines what triggers conversation generation"""
    name = models.CharField(max_length=50)
    description = models.TextField()
    
    trigger_type = models.CharField(
        max_length=30,
        choices=[
            ('usage_threshold', 'Usage Threshold'),
            ('pattern_detected', 'Pattern Detected'),
            ('app_milestone', 'App Milestone'),
            ('time_based', 'Time Based'),
            ('social_event', 'Social Event'),
            ('goal_progress', 'Goal Progress'),
            ('device_event', 'Device Event'),
            ('manual', 'Manual Trigger')
        ]
    )
    
    # Trigger conditions (JSON configuration)
    conditions = models.JSONField(default=dict, help_text="Conditions that must be met")
    
    # Trigger settings
    priority = models.IntegerField(default=5, help_text="1-10 priority level")
    cooldown_hours = models.IntegerField(default=24, help_text="Hours before trigger can fire again")
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Conversation(models.Model):
    """AI-generated conversations between devices and apps"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    
    # Conversation metadata
    title = models.CharField(max_length=200, blank=True)
    date = models.DateField(default=timezone.now)
    conversation_type = models.CharField(
        max_length=30,
        choices=[
            ('daily_recap', 'Daily Recap'),
            ('usage_intervention', 'Usage Intervention'),
            ('pattern_discussion', 'Pattern Discussion'),
            ('goal_check_in', 'Goal Check-in'),
            ('app_drama', 'App Drama'),
            ('device_gossip', 'Device Gossip'),
            ('productivity_roast', 'Productivity Roast'),
            ('social_comparison', 'Social Comparison'),
            ('milestone_celebration', 'Milestone Celebration'),
            ('friend_visit', 'Friend Device Visit'),
            ('emergency_meeting', 'Emergency Meeting')
        ]
    )
    
    # Participants
    participating_devices = models.ManyToManyField('devices.Device', blank=True)
    participating_apps = models.ManyToManyField('apps.DeviceApp', blank=True)
    guest_devices = models.ManyToManyField('social.TemporaryDevice', blank=True)
    
    # Content
    content = models.TextField(help_text="The full conversation content")
    summary = models.TextField(blank=True, help_text="Brief summary of conversation")
    
    # Conversation characteristics
    mood = models.CharField(
        max_length=20,
        choices=[
            ('humorous', 'Humorous'),
            ('supportive', 'Supportive'),
            ('dramatic', 'Dramatic'),
            ('sarcastic', 'Sarcastic'),
            ('educational', 'Educational'),
            ('gossipy', 'Gossipy'),
            ('competitive', 'Competitive'),
            ('concerned', 'Concerned'),
            ('celebratory', 'Celebratory'),
            ('chaotic', 'Chaotic')
        ],
        default='humorous'
    )
    
    # Triggers and context
    triggers = models.ManyToManyField(ConversationTrigger, blank=True)
    trigger_data = models.JSONField(default=dict, help_text="Data that triggered this conversation")
    
    # AI generation details
    ai_model_used = models.CharField(max_length=50, blank=True)
    generation_prompt = models.TextField(blank=True)
    generation_tokens = models.IntegerField(null=True, blank=True)
    generation_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    
    # User interaction
    user_rating = models.IntegerField(null=True, blank=True, help_text="1-5 star rating")
    user_feedback = models.TextField(blank=True)
    is_favorite = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    
    # Status
    generation_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Generation'),
            ('generating', 'Currently Generating'),
            ('completed', 'Completed'),
            ('failed', 'Generation Failed'),
            ('retry', 'Retry Needed')
        ],
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.conversation_type} - {self.date}"
    
    @property
    def participant_count(self):
        return self.participating_devices.count() + self.participating_apps.count()
    
    @property
    def word_count(self):
        return len(self.content.split()) if self.content else 0

class DeviceJournal(models.Model):
    """Individual device journal entries"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, related_name='journal_entries')
    date = models.DateField()
    
    # Journal content
    content = models.TextField(help_text="The device's perspective on the day")
    mood = models.CharField(
        max_length=20,
        choices=[
            ('happy', 'Happy'),
            ('frustrated', 'Frustrated'),
            ('proud', 'Proud'),
            ('tired', 'Tired'),
            ('excited', 'Excited'),
            ('confused', 'Confused'),
            ('satisfied', 'Satisfied'),
            ('overwhelmed', 'Overwhelmed'),
            ('bored', 'Bored'),
            ('grateful', 'Grateful')
        ]
    )
    
    # Key events and insights
    notable_events = models.JSONField(default=list, help_text="List of notable events")
    insights = models.TextField(blank=True, help_text="Device's insights about usage patterns")
    
    # Relationships and interactions
    mentioned_apps = models.ManyToManyField('apps.DeviceApp', blank=True)
    mentioned_devices = models.ManyToManyField('devices.Device', blank=True)
    
    # Usage context
    usage_summary = models.JSONField(default=dict, help_text="Summary of day's usage")
    personality_development = models.TextField(blank=True, help_text="How personality evolved")
    
    # AI generation details
    ai_generated = models.BooleanField(default=True)
    generation_prompt = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['device', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.device.name} Journal - {self.date}"

class AppJournal(models.Model):
    """Individual app journal entries"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_app = models.ForeignKey('apps.DeviceApp', on_delete=models.CASCADE, related_name='journal_entries')
    date = models.DateField()
    
    # Journal content
    content = models.TextField(help_text="The app's perspective on the day")
    mood = models.CharField(
        max_length=20,
        choices=[
            ('satisfied', 'Satisfied'),
            ('neglected', 'Neglected'),
            ('overused', 'Overused'),
            ('appreciated', 'Appreciated'),
            ('frustrated', 'Frustrated'),
            ('excited', 'Excited'),
            ('jealous', 'Jealous'),
            ('proud', 'Proud'),
            ('worried', 'Worried'),
            ('content', 'Content')
        ]
    )
    
    # App-specific experiences
    session_highlights = models.JSONField(default=list, help_text="Highlights from usage sessions")
    user_behavior_notes = models.TextField(blank=True, help_text="Observations about user behavior")
    
    # Relationships
    app_interactions = models.JSONField(default=dict, help_text="Interactions with other apps")
    mentioned_apps = models.ManyToManyField('apps.DeviceApp', blank=True)
    
    # Usage reflection
    usage_satisfaction = models.IntegerField(null=True, blank=True, help_text="1-10 satisfaction with usage")
    productivity_contribution = models.IntegerField(null=True, blank=True, help_text="1-10 productivity contribution")
    
    # AI generation
    ai_generated = models.BooleanField(default=True)
    generation_prompt = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['device_app', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.device_app.display_name} Journal - {self.date}"

class ConversationTemplate(models.Model):
    """Templates for generating different types of conversations"""
    name = models.CharField(max_length=100)
    conversation_type = models.CharField(max_length=30)
    
    # Template content
    system_prompt = models.TextField(help_text="System prompt for AI")
    user_prompt_template = models.TextField(help_text="User prompt template with placeholders")
    
    # Template settings
    max_participants = models.IntegerField(default=5)
    min_participants = models.IntegerField(default=2)
    preferred_mood = models.CharField(max_length=20, blank=True)
    
    # Usage conditions
    usage_requirements = models.JSONField(default=dict, help_text="Requirements for using this template")
    
    # Template metadata
    version = models.CharField(max_length=10, default='1.0')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (v{self.version})"

class ConversationFeedback(models.Model):
    """User feedback on conversations for improving AI generation"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Feedback ratings
    accuracy_rating = models.IntegerField(help_text="1-5 accuracy of usage data representation")
    humor_rating = models.IntegerField(help_text="1-5 humor quality")
    personality_rating = models.IntegerField(help_text="1-5 personality consistency")
    overall_rating = models.IntegerField(help_text="1-5 overall satisfaction")
    
    # Detailed feedback
    what_worked = models.TextField(blank=True)
    what_didnt_work = models.TextField(blank=True)
    suggestions = models.TextField(blank=True)
    
    # Feedback categories
    feedback_categories = models.JSONField(default=list, help_text="Categories of feedback")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for {self.conversation.id} - {self.overall_rating}/5"