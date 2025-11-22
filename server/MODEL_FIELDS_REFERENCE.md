# Model Fields Quick Reference

This file shows the actual field names in each model for quick comparison when fixing admin.py files.

---

## applications.App

**Location:** `server/apps/applications/models.py`

**Actual Fields:**
```python
class App(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    bundle_id = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(AppCategory, on_delete=models.SET_NULL, null=True)
    
    # Platform identifiers
    ios_bundle_id = models.CharField(max_length=200, blank=True)
    android_package = models.CharField(max_length=200, blank=True)
    windows_exe = models.CharField(max_length=200, blank=True)
    mac_bundle_id = models.CharField(max_length=200, blank=True)
    
    # Display
    icon_url = models.URLField(blank=True)  # ← NOT 'icon'
    primary_color = models.CharField(max_length=7, blank=True)
    
    # Personality
    default_personality = models.CharField(max_length=30, choices=[...])
    personality_description = models.TextField(blank=True)
    
    # Characteristics
    is_social_media = models.BooleanField(default=False)
    is_productivity = models.BooleanField(default=False)
    is_entertainment = models.BooleanField(default=False)
    is_work_related = models.BooleanField(default=False)
    is_game = models.BooleanField(default=False)
    
    typical_session_length = models.IntegerField(null=True, blank=True)
    addictive_potential = models.IntegerField(default=5)
    productivity_score = models.IntegerField(default=5)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Admin Fix:**
- `icon` → `icon_url`

---

## applications.AppRelationship

**Location:** `server/apps/applications/models.py`

**Actual Fields:**
```python
class AppRelationship(models.Model):
    app_a = models.ForeignKey(App, on_delete=models.CASCADE, related_name='relationships_as_a')  # ← NOT 'app1'
    app_b = models.ForeignKey(App, on_delete=models.CASCADE, related_name='relationships_as_b')  # ← NOT 'app2'
    
    relationship_type = models.CharField(max_length=30, choices=[...])
    intensity = models.IntegerField(default=5)  # ← NOT 'strength'
    notes = models.TextField(blank=True)
    
    interactions_count = models.IntegerField(default=0)
    last_interaction = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Admin Fix:**
- `app1` → `app_a`
- `app2` → `app_b`
- `strength` → `intensity`

---

## applications.DeviceApp

**Location:** `server/apps/applications/models.py`

**Actual Fields:**
```python
class DeviceApp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, related_name='device_apps')
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='device_installations')
    
    # Custom naming
    display_name = models.CharField(max_length=100, blank=True)
    custom_icon = models.URLField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)  # ← NOT 'is_installed'
    installed_at = models.DateTimeField(default=timezone.now)  # ← NOT 'install_date'
    last_used = models.DateTimeField(null=True, blank=True)
    
    # Usage tracking
    total_usage_time = models.IntegerField(default=0)
    launch_count = models.IntegerField(default=0)
    
    # Custom personality override
    personality_override = models.CharField(max_length=30, blank=True)
    personality_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Admin Fix:**
- `install_date` → `installed_at`
- `is_installed` → `is_active`

---

## conversations.Conversation

**Location:** `server/apps/conversations/models.py`

**Actual Fields:**
```python
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    
    # Metadata
    title = models.CharField(max_length=200, blank=True)
    date = models.DateField(default=timezone.now)
    conversation_type = models.CharField(max_length=30, choices=[...])
    
    # Participants
    participating_devices = models.ManyToManyField('devices.Device', blank=True)
    participating_apps = models.ManyToManyField('applications.DeviceApp', blank=True)
    guest_devices = models.ManyToManyField('social.TemporaryDeviceConnection', blank=True)
    
    # Content
    content = models.TextField()
    summary = models.TextField(blank=True)
    mood = models.CharField(max_length=20, choices=[...])
    
    # Triggers
    triggers = models.ManyToManyField(ConversationTrigger, blank=True)
    trigger_data = models.JSONField(default=dict)
    
    # AI generation details
    ai_model_used = models.CharField(max_length=50, blank=True)  # ← NOT 'model_used'
    generation_prompt = models.TextField(blank=True)
    generation_tokens = models.IntegerField(null=True, blank=True)  # ← NOT 'tokens_used'
    generation_cost = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    
    # User interaction
    user_rating = models.IntegerField(null=True, blank=True)  # ← NOT 'rating'
    user_feedback = models.TextField(blank=True)
    is_favorite = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    
    # Status
    generation_status = models.CharField(max_length=20, choices=[...])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Admin Fix:**
- `model_used` → `ai_model_used`
- `tokens_used` → `generation_tokens`
- `rating` → `user_rating`
- Remove `is_read` (doesn't exist - use `is_hidden` or `generation_status` instead)
- Remove `is_ai_generated` (use `generation_status` instead)

---

## conversations.ConversationTrigger

**Location:** `server/apps/conversations/models.py`

**Actual Fields:**
```python
class ConversationTrigger(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    trigger_type = models.CharField(max_length=30, choices=[...])
    
    # Trigger conditions (JSON configuration)
    conditions = models.JSONField(default=dict)  # ← NOT 'condition' (singular)
    
    # Trigger settings
    priority = models.IntegerField(default=5)
    cooldown_hours = models.IntegerField(default=24)
    is_active = models.BooleanField(default=True)
    
    # NO created_at or updated_at fields!
```

**Admin Fix:**
- `condition` → `conditions`
- Remove `created_at` (doesn't exist)

---

## conversations.DeviceJournal

**Location:** `server/apps/conversations/models.py`

**Actual Fields:**
```python
class DeviceJournal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey('devices.Device', on_delete=models.CASCADE, related_name='journal_entries')
    date = models.DateField()
    
    # Journal content
    content = models.TextField()
    mood = models.CharField(max_length=20, choices=[...])
    
    # Key events and insights
    notable_events = models.JSONField(default=list)
    insights = models.TextField(blank=True)
    
    # Relationships
    mentioned_apps = models.ManyToManyField('applications.DeviceApp', blank=True)
    mentioned_devices = models.ManyToManyField('devices.Device', blank=True)
    
    # Usage context
    usage_summary = models.JSONField(default=dict)
    personality_development = models.TextField(blank=True)
    
    # AI generation details
    ai_generated = models.BooleanField(default=True)  # ← NOT 'is_ai_generated'
    generation_prompt = models.TextField(blank=True)
    # NO 'model_used' field!
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Admin Fix:**
- `is_ai_generated` → `ai_generated`
- Remove `model_used` (doesn't exist)

---

## conversations.AppJournal

**Location:** `server/apps/conversations/models.py`

**Actual Fields:**
```python
class AppJournal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_app = models.ForeignKey('applications.DeviceApp', on_delete=models.CASCADE, related_name='journal_entries')
    date = models.DateField()
    
    # Journal content
    content = models.TextField()
    mood = models.CharField(max_length=20, choices=[...])
    
    # App-specific experiences
    session_highlights = models.JSONField(default=list)
    user_behavior_notes = models.TextField(blank=True)
    
    # Relationships
    app_interactions = models.JSONField(default=dict)
    mentioned_apps = models.ManyToManyField('applications.DeviceApp', blank=True)
    
    # Usage reflection
    usage_satisfaction = models.IntegerField(null=True, blank=True)
    productivity_contribution = models.IntegerField(null=True, blank=True)
    
    # AI generation
    ai_generated = models.BooleanField(default=True)  # ← NOT 'is_ai_generated'
    generation_prompt = models.TextField(blank=True)
    # NO 'model_used' field!
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Admin Fix:**
- `is_ai_generated` → `ai_generated`
- Remove `model_used` (doesn't exist)

---

## conversations.ConversationFeedback

**Note:** This model may NOT exist in the models.py file!

Check `server/apps/conversations/models.py` for this model. If it doesn't exist, **remove the entire ConversationFeedbackAdmin class** from admin.py.

---

## Summary of Common Patterns

### Pattern 1: Boolean field naming
- Admin uses: `is_ai_generated`
- Model has: `ai_generated`
- **Fix:** Remove `is_` prefix

### Pattern 2: AI model field
- Admin uses: `model_used`
- Model has: `ai_model_used` (or doesn't exist)
- **Fix:** Add `ai_` prefix or remove if doesn't exist

### Pattern 3: Relationship fields
- Admin uses: `app1`, `app2`, `device1`, `device2`
- Model has: `app_a`, `app_b`, `device_a`, `device_b`
- **Fix:** Use `_a` and `_b` suffixes

### Pattern 4: Date/time fields
- Admin uses: `install_date`, `created_at`
- Model has: `installed_at` (or field doesn't exist)
- **Fix:** Use `_at` suffix or check if field exists

### Pattern 5: Singular vs Plural
- Admin uses: `condition` (singular)
- Model has: `conditions` (plural, usually JSONField)
- **Fix:** Use plural form

---

## Testing Your Fixes

After making changes to admin.py files:

```bash
# 1. Check for errors
python manage.py check

# 2. If no errors, create migrations
python manage.py makemigrations

# 3. Review migrations
python manage.py showmigrations

# 4. Apply migrations
python manage.py migrate
```

