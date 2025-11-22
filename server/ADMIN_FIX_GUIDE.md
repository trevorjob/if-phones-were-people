# Step-by-Step Admin Fix Guide for AI IDE

This guide provides exact instructions for fixing each admin.py file. Copy and paste the file paths and changes to your AI IDE.

---

## File 1: server/apps/applications/admin.py

### Change 1: AppAdmin - Fix icon field
**Line to find:**
```python
list_display = ['name', 'category', 'bundle_id', 'icon', 'default_personality']
```

**Replace with:**
```python
list_display = ['name', 'category', 'bundle_id', 'icon_url', 'default_personality']
```

---

### Change 2: AppRelationshipAdmin - Fix field names
**Line to find:**
```python
list_display = ['app1', 'app2', 'relationship_type', 'strength', 'created_at']
```

**Replace with:**
```python
list_display = ['app_a', 'app_b', 'relationship_type', 'intensity', 'created_at']
```

**Also find:**
```python
search_fields = ['app1__name', 'app2__name']
```

**Replace with:**
```python
search_fields = ['app_a__name', 'app_b__name']
```

---

### Change 3: DeviceAppAdmin - Fix install_date and is_installed
**In readonly_fields, find:**
```python
readonly_fields = ['install_date', 'updated_at']
```

**Replace with:**
```python
readonly_fields = ['installed_at', 'created_at', 'updated_at']
```

**In list_display, find:**
```python
list_display = ['device', 'app', 'display_name', 'is_installed', 'usage_time', 'install_date']
```

**Replace with:**
```python
list_display = ['device', 'app', 'display_name', 'is_active', 'total_usage_time', 'installed_at']
```

**In list_filter, find:**
```python
list_filter = ['is_installed', 'device', 'install_date']
```

**Replace with:**
```python
list_filter = ['is_active', 'device', 'installed_at']
```

**In fieldsets, find:**
```python
'fields': ('device', 'app', 'display_name', 'is_installed', 'install_date')
```

**Replace with:**
```python
'fields': ('device', 'app', 'display_name', 'is_active', 'installed_at')
```

---

## File 2: server/apps/conversations/admin.py

### Change 1: ConversationAdmin - Fix model_used and tokens_used
**In readonly_fields, find:**
```python
readonly_fields = ['created_at', 'model_used', 'tokens_used']
```

**Replace with:**
```python
readonly_fields = ['created_at', 'ai_model_used', 'generation_tokens']
```

**In list_display, find:**
```python
list_display = ['user', 'conversation_type', 'date', 'mood', 'is_read', 'is_favorite', 'rating']
```

**Replace with:**
```python
list_display = ['user', 'conversation_type', 'date', 'mood', 'is_favorite', 'user_rating', 'generation_status']
```

**In list_filter, find:**
```python
list_filter = ['conversation_type', 'mood', 'is_read', 'date', 'is_ai_generated']
```

**Replace with:**
```python
list_filter = ['conversation_type', 'mood', 'generation_status', 'date']
```

**In fieldsets, find the AI generation section:**
```python
('AI Generation', {
    'fields': ('is_ai_generated', 'model_used', 'generation_prompt', 'tokens_used', 'generation_cost'),
```

**Replace with:**
```python
('AI Generation', {
    'fields': ('generation_status', 'ai_model_used', 'generation_prompt', 'generation_tokens', 'generation_cost'),
```

---

### Change 2: ConversationTriggerAdmin - Fix condition and created_at
**In list_display, find:**
```python
list_display = ['name', 'condition', 'is_active', 'created_at']
```

**Replace with:**
```python
list_display = ['name', 'trigger_type', 'is_active', 'priority']
```

**In list_filter, find:**
```python
list_filter = ['is_active', 'trigger_type', 'created_at']
```

**Replace with:**
```python
list_filter = ['is_active', 'trigger_type', 'priority']
```

**In fieldsets, find:**
```python
('Trigger Details', {
    'fields': ('trigger_type', 'condition', 'priority', 'cooldown_hours')
```

**Replace with:**
```python
('Trigger Details', {
    'fields': ('trigger_type', 'conditions', 'priority', 'cooldown_hours')
```

**Also remove the Timestamps fieldset completely** (ConversationTrigger has no timestamps):
```python
# Remove this entire section:
('Timestamps', {
    'fields': ('created_at',),
    'classes': ('collapse',)
}),
```

---

### Change 3: DeviceJournalAdmin - Fix is_ai_generated and model_used
**In readonly_fields, find:**
```python
readonly_fields = ['created_at', 'model_used']
```

**Replace with:**
```python
readonly_fields = ['created_at', 'updated_at']
```

**In list_display, find:**
```python
list_display = ['device', 'date', 'mood', 'is_ai_generated', 'created_at']
```

**Replace with:**
```python
list_display = ['device', 'date', 'mood', 'ai_generated', 'created_at']
```

**In list_filter, find:**
```python
list_filter = ['mood', 'is_ai_generated', 'date']
```

**Replace with:**
```python
list_filter = ['mood', 'ai_generated', 'date']
```

**In fieldsets, find:**
```python
('AI Generation', {
    'fields': ('is_ai_generated', 'model_used', 'generation_prompt'),
```

**Replace with:**
```python
('AI Generation', {
    'fields': ('ai_generated', 'generation_prompt'),
```

---

### Change 4: AppJournalAdmin - Fix is_ai_generated and model_used
**In readonly_fields, find:**
```python
readonly_fields = ['created_at', 'model_used']
```

**Replace with:**
```python
readonly_fields = ['created_at', 'updated_at']
```

**In list_display, find:**
```python
list_display = ['device_app', 'date', 'mood', 'is_ai_generated', 'created_at']
```

**Replace with:**
```python
list_display = ['device_app', 'date', 'mood', 'ai_generated', 'created_at']
```

**In list_filter, find:**
```python
list_filter = ['mood', 'is_ai_generated', 'date']
```

**Replace with:**
```python
list_filter = ['mood', 'ai_generated', 'date']
```

**In fieldsets, find:**
```python
('AI Generation', {
    'fields': ('is_ai_generated', 'model_used', 'generation_prompt'),
```

**Replace with:**
```python
('AI Generation', {
    'fields': ('ai_generated', 'generation_prompt'),
```

---

### Change 5: ConversationFeedbackAdmin - Check if model exists

**First, check if `ConversationFeedback` model exists in `server/apps/conversations/models.py`**

If the model DOES NOT EXIST, **remove the entire admin class**:
```python
# Remove this entire section:
@admin.register(ConversationFeedback)
class ConversationFeedbackAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'rating', 'feedback_type', 'created_at']
    list_filter = ['rating', 'feedback_type', 'created_at']
    search_fields = ['conversation__title']
    readonly_fields = ['created_at']
```

**Also remove the import** at the top of the file:
```python
# In the import statement, remove ConversationFeedback:
from .models import Conversation, ConversationTrigger, DeviceJournal, AppJournal
# Remove ConversationFeedback from this line
```

---

## Verification Commands

After making all changes, run these commands in order:

### 1. Check for admin errors
```powershell
cd C:\Users\HP\Videos\programming\if-phones-were-people\server
.\venv\Scripts\Activate.ps1
python manage.py check
```

**Expected output:** No errors (or only security warnings)

### 2. Create migrations
```powershell
python manage.py makemigrations
```

**Expected output:** Migration files created for each app

### 3. Show migrations
```powershell
python manage.py showmigrations
```

**Expected output:** List of all migrations with checkboxes

---

## Quick Summary

| File | Changes | Lines to Modify |
|------|---------|----------------|
| `applications/admin.py` | 3 classes, ~8 changes | AppAdmin, AppRelationshipAdmin, DeviceAppAdmin |
| `conversations/admin.py` | 5 classes, ~15 changes | ConversationAdmin, ConversationTriggerAdmin, DeviceJournalAdmin, AppJournalAdmin, ConversationFeedbackAdmin |

**Total Changes:** ~23 line modifications across 2 files

**Time Estimate:** 10-15 minutes with AI IDE assistance

---

## Common Patterns to Remember

1. **`is_` prefix removal**: `is_ai_generated` → `ai_generated`
2. **`_a/_b` suffixes**: `app1/app2` → `app_a/app_b`
3. **`_at` suffix**: `install_date` → `installed_at`
4. **AI fields**: `model_used` → `ai_model_used`, `tokens_used` → `generation_tokens`
5. **User fields**: `rating` → `user_rating`
6. **Plural forms**: `condition` → `conditions`

---

## If You Get Stuck

1. **Reference the model files** in `server/apps/*/models.py`
2. **Check the error message** - it tells you exactly which field is wrong
3. **Search for the field name** in the model file to see what it's actually called
4. **Use MODEL_FIELDS_REFERENCE.md** for quick field name lookup

