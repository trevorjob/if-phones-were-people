from django.db import models
from django.utils import timezone

class ConversationPrompt(models.Model):
    """Templates for AI conversation generation"""
    name = models.CharField(max_length=100, unique=True)
    template = models.TextField()
    description = models.TextField(blank=True)
    
    # Applicability
    trigger_types = models.JSONField(default=list)  # Which triggers this applies to
    personality_modifiers = models.JSONField(default=dict)
    
    # Versioning
    version = models.CharField(max_length=10, default='1.0')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} v{self.version}"


class AIGenerationLog(models.Model):
    """Log of AI generation requests for debugging and optimization"""
    content_type = models.CharField(max_length=20)  # 'conversation', 'journal_device', 'journal_app'
    content_id = models.CharField(max_length=50)  # UUID or ID of generated content
    
    # Request details
    model_used = models.CharField(max_length=50)
    prompt_used = models.TextField()
    input_data = models.JSONField()
    
    # Response details
    generated_content = models.TextField()
    generation_time = models.DurationField()
    tokens_used = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    
    # Quality metrics
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    user_rating = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'created_at']),
            models.Index(fields=['model_used', 'success']),
        ]
    
    def __str__(self):
        return f"{self.content_type} - {self.model_used} - {self.created_at}"
