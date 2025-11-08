# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
import uuid

class User(AbstractUser):
    """Extended user model with additional fields for the app"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=50, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Privacy settings
    allow_friend_requests = models.BooleanField(default=True)
    share_usage_stats = models.BooleanField(default=False)
    public_profile = models.BooleanField(default=False)
    
    # API keys for data collection
    api_key = models.CharField(max_length=100, unique=True, blank=True)
    ios_shortcut_id = models.CharField(max_length=100, blank=True)
    
    # Usage preferences
    conversation_frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('interesting', 'Only for interesting patterns'),
            ('off', 'Disabled')
        ],
        default='daily'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.display_name or self.username
    
    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = self.generate_api_key()
        super().save(*args, **kwargs)
    
    def generate_api_key(self):
        """Generate a unique API key for this user"""
        return f"ipwp_{uuid.uuid4().hex[:24]}"
    
    @property
    def active_devices(self):
        return self.devices.filter(is_active=True)
    
    @property
    def total_screen_time_today(self):
        from usage.models import UsageData
        from django.utils import timezone
        
        today = timezone.now().date()
        usage_data = UsageData.objects.filter(
            device__user=self,
            date=today
        ).aggregate(
            total=models.Sum('total_screen_time')
        )
        return usage_data['total'] or 0

class UserProfile(models.Model):
    """Extended profile information for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal preferences
    favorite_device_type = models.CharField(
        max_length=20,
        choices=[
            ('phone', 'Phone'),
            ('laptop', 'Laptop'),
            ('tablet', 'Tablet'),
            ('desktop', 'Desktop')
        ],
        blank=True
    )
    
    digital_wellness_goal = models.CharField(
        max_length=30,
        choices=[
            ('reduce_usage', 'Reduce overall usage'),
            ('be_productive', 'Be more productive'),
            ('balance', 'Better work-life balance'),
            ('mindful', 'Mindful usage'),
            ('none', 'No specific goal')
        ],
        default='none'
    )
    
    # Social settings
    friend_code = models.CharField(max_length=12, unique=True, blank=True)
    allow_device_invites = models.BooleanField(default=True)
    auto_accept_close_friends = models.BooleanField(default=False)
    
    # Notification preferences
    daily_summary_enabled = models.BooleanField(default=True)
    conversation_notifications = models.BooleanField(default=True)
    weekly_insights = models.BooleanField(default=True)
    friend_activity_notifications = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        if not self.friend_code:
            self.friend_code = self.generate_friend_code()
        super().save(*args, **kwargs)
    
    def generate_friend_code(self):
        """Generate a unique 12-character friend code"""
        import random
        import string
        
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            if not UserProfile.objects.filter(friend_code=code).exists():
                return code