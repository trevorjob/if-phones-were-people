# Django Admin Configuration Errors - Detailed Report

**Generated:** November 13, 2025  
**Total Issues:** 28 errors (0 silenced)

This document lists all Django admin configuration errors that need to be fixed. Each error indicates a mismatch between the admin.py configuration and the actual model fields.

---

## Summary by App

| App | Errors | Models Affected |
|-----|--------|----------------|
| applications | 9 | App, AppRelationship, DeviceApp |
| conversations | 15 | AppJournal, Conversation, ConversationFeedback, ConversationTrigger, DeviceJournal |
| (other apps) | 4+ | Various |

---

## 1. applications.App

**File:** `server/apps/applications/admin.py`  
**Admin Class:** `AppAdmin`

### Error 1: Missing 'icon' field
```
<class 'apps.applications.admin.AppAdmin'>: (admin.E108) 
The value of 'list_display[4]' refers to 'icon', which is not a callable 
or attribute of 'AppAdmin', or an attribute, method, or field on 'applications.App'.
```

**Issue:** Admin references `icon` but the model has `icon_url` instead.

**Current Admin Config:**
```python
list_display = ['name', 'category', 'bundle_id', 'icon', ...]
```

**Model Field Name:**
```python
icon_url = models.URLField(blank=True)
```

**Fix:** Change `'icon'` to `'icon_url'` in list_display

---

## 2. applications.AppRelationship

**File:** `server/apps/applications/admin.py`  
**Admin Class:** `AppRelationshipAdmin`

### Error 2-4: Wrong field names for apps and strength

```
<class 'apps.applications.admin.AppRelationshipAdmin'>: (admin.E108) 
The value of 'list_display[0]' refers to 'app1', which is not a callable...

<class 'apps.applications.admin.AppRelationshipAdmin'>: (admin.E108) 
The value of 'list_display[1]' refers to 'app2', which is not a callable...

<class 'apps.applications.admin.AppRelationshipAdmin'>: (admin.E108) 
The value of 'list_display[3]' refers to 'strength', which is not a callable...
```

**Issue:** Admin uses `app1`, `app2`, `strength` but model has different field names.

**Current Admin Config:**
```python
list_display = ['app1', 'app2', 'relationship_type', 'strength', 'created_at']
```

**Actual Model Fields:**
- Model needs to be checked for actual field names
- Likely `app_a`, `app_b`, `intensity` or similar

**Fix:** Update list_display to match actual model field names

---

## 3. applications.DeviceApp

**File:** `server/apps/applications/admin.py`  
**Admin Class:** `DeviceAppAdmin`

### Error 5-9: Multiple field name mismatches

```
<class 'apps.applications.admin.DeviceAppAdmin'>: (admin.E035) 
The value of 'readonly_fields[0]' refers to 'install_date'...

<class 'apps.applications.admin.DeviceAppAdmin'>: (admin.E108) 
The value of 'list_display[3]' refers to 'is_installed'...

<class 'apps.applications.admin.DeviceAppAdmin'>: (admin.E108) 
The value of 'list_display[5]' refers to 'install_date'...

<class 'apps.applications.admin.DeviceAppAdmin'>: (admin.E116) 
The value of 'list_filter[0]' refers to 'is_installed'...

<class 'apps.applications.admin.DeviceAppAdmin'>: (admin.E116) 
The value of 'list_filter[2]' refers to 'install_date'...
```

**Issue:** Admin references `install_date` and `is_installed` which don't exist in model.

**Current Admin Config:**
```python
readonly_fields = ['install_date', 'updated_at']
list_display = ['device', 'app', 'display_name', 'is_installed', 'usage_time', 'install_date']
list_filter = ['is_installed', 'device', 'install_date']
```

**Actual Model Fields:**
- Model has `installed_at` instead of `install_date`
- Model has `is_active` instead of `is_installed`

**Fix:** 
- Change all `install_date` → `installed_at`
- Change all `is_installed` → `is_active`

---

## 4. conversations.AppJournal

**File:** `server/apps/conversations/admin.py`  
**Admin Class:** `AppJournalAdmin`

### Error 10-12: Field name mismatches

```
<class 'apps.conversations.admin.AppJournalAdmin'>: (admin.E035) 
The value of 'readonly_fields[1]' refers to 'model_used'...

<class 'apps.conversations.admin.AppJournalAdmin'>: (admin.E108) 
The value of 'list_display[3]' refers to 'is_ai_generated'...

<class 'apps.conversations.admin.AppJournalAdmin'>: (admin.E116) 
The value of 'list_filter[1]' refers to 'is_ai_generated'...
```

**Issue:** Admin references fields that don't exist in model.

**Current Admin Config:**
```python
readonly_fields = ['created_at', 'model_used']
list_display = ['device_app', 'date', 'mood', 'is_ai_generated', 'created_at']
list_filter = ['mood', 'is_ai_generated', 'date']
```

**Actual Model Fields:**
- Model has `ai_generated` not `is_ai_generated`
- Model doesn't have `model_used` field

**Fix:**
- Change `is_ai_generated` → `ai_generated`
- Remove `model_used` from readonly_fields

---

## 5. conversations.Conversation

**File:** `server/apps/conversations/admin.py`  
**Admin Class:** `ConversationAdmin`

### Error 13-18: Multiple field mismatches

```
<class 'apps.conversations.admin.ConversationAdmin'>: (admin.E035) 
The value of 'readonly_fields[1]' refers to 'model_used'...

<class 'apps.conversations.admin.ConversationAdmin'>: (admin.E035) 
The value of 'readonly_fields[2]' refers to 'tokens_used'...

<class 'apps.conversations.admin.ConversationAdmin'>: (admin.E108) 
The value of 'list_display[4]' refers to 'is_read'...

<class 'apps.conversations.admin.ConversationAdmin'>: (admin.E108) 
The value of 'list_display[6]' refers to 'rating'...

<class 'apps.conversations.admin.ConversationAdmin'>: (admin.E116) 
The value of 'list_filter[2]' refers to 'is_read'...

<class 'apps.conversations.admin.ConversationAdmin'>: (admin.E116) 
The value of 'list_filter[4]' refers to 'is_ai_generated'...
```

**Issue:** Multiple field name mismatches.

**Current Admin Config:**
```python
readonly_fields = ['created_at', 'model_used', 'tokens_used']
list_display = ['user', 'conversation_type', 'date', 'mood', 'is_read', 'is_favorite', 'rating']
list_filter = ['conversation_type', 'mood', 'is_read', 'date', 'is_ai_generated']
```

**Actual Model Fields:**
- Model has `ai_model_used` not `model_used`
- Model has `generation_tokens` not `tokens_used`
- Model has `user_rating` not `rating`
- Model has `is_hidden` but likely not `is_read`
- Model has `generation_status` but not `is_ai_generated`

**Fix:**
- Change `model_used` → `ai_model_used`
- Change `tokens_used` → `generation_tokens`
- Change `rating` → `user_rating`
- Remove or replace `is_read` (check model for actual field)
- Remove `is_ai_generated` from list_filter

---

## 6. conversations.ConversationFeedback

**File:** `server/apps/conversations/admin.py`  
**Admin Class:** `ConversationFeedbackAdmin`

### Error 19-22: Field name mismatches

```
<class 'apps.conversations.admin.ConversationFeedbackAdmin'>: (admin.E108) 
The value of 'list_display[1]' refers to 'rating'...

<class 'apps.conversations.admin.ConversationFeedbackAdmin'>: (admin.E108) 
The value of 'list_display[2]' refers to 'feedback_type'...

<class 'apps.conversations.admin.ConversationFeedbackAdmin'>: (admin.E116) 
The value of 'list_filter[0]' refers to 'rating'...

<class 'apps.conversations.admin.ConversationFeedbackAdmin'>: (admin.E116) 
The value of 'list_filter[1]' refers to 'feedback_type'...
```

**Issue:** ConversationFeedback model may not exist or has different field names.

**Current Admin Config:**
```python
list_display = ['conversation', 'rating', 'feedback_type', 'created_at']
list_filter = ['rating', 'feedback_type', 'created_at']
```

**Fix:** Check if ConversationFeedback model exists. If not, remove this admin class.

---

## 7. conversations.ConversationTrigger

**File:** `server/apps/conversations/admin.py`  
**Admin Class:** `ConversationTriggerAdmin`

### Error 23-25: Field name mismatches

```
<class 'apps.conversations.admin.ConversationTriggerAdmin'>: (admin.E108) 
The value of 'list_display[1]' refers to 'condition'...

<class 'apps.conversations.admin.ConversationTriggerAdmin'>: (admin.E108) 
The value of 'list_display[3]' refers to 'created_at'...

<class 'apps.conversations.admin.ConversationTriggerAdmin'>: (admin.E116) 
The value of 'list_filter[2]' refers to 'created_at'...
```

**Issue:** Model doesn't have `condition` or `created_at` fields.

**Current Admin Config:**
```python
list_display = ['name', 'condition', 'is_active', 'created_at']
list_filter = ['is_active', 'trigger_type', 'created_at']
```

**Actual Model Fields:**
- Model has `conditions` (JSON field) not `condition`
- Model likely has no `created_at` timestamp

**Fix:**
- Change `condition` → `conditions`
- Remove `created_at` from list_display and list_filter

---

## 8. conversations.DeviceJournal

**File:** `server/apps/conversations/admin.py`  
**Admin Class:** `DeviceJournalAdmin`

### Error 26-28: Field name mismatches

```
<class 'apps.conversations.admin.DeviceJournalAdmin'>: (admin.E035) 
The value of 'readonly_fields[1]' refers to 'model_used'...

<class 'apps.conversations.admin.DeviceJournalAdmin'>: (admin.E108) 
The value of 'list_display[3]' refers to 'is_ai_generated'...

<class 'apps.conversations.admin.DeviceJournalAdmin'>: (admin.E116) 
The value of 'list_filter[1]' refers to 'is_ai_generated'...
```

**Issue:** Same pattern as AppJournal - wrong field names.

**Current Admin Config:**
```python
readonly_fields = ['created_at', 'model_used']
list_display = ['device', 'date', 'mood', 'is_ai_generated', 'created_at']
list_filter = ['mood', 'is_ai_generated', 'date']
```

**Actual Model Fields:**
- Model has `ai_generated` not `is_ai_generated`
- Model doesn't have `model_used`

**Fix:**
- Change `is_ai_generated` → `ai_generated`
- Remove `model_used` from readonly_fields

---

## Quick Fix Checklist

### applications/admin.py
- [ ] Change `icon` → `icon_url` in AppAdmin
- [ ] Fix AppRelationship field names (check model first)
- [ ] Change `install_date` → `installed_at` in DeviceAppAdmin
- [ ] Change `is_installed` → `is_active` in DeviceAppAdmin

### conversations/admin.py
- [ ] Change `is_ai_generated` → `ai_generated` in AppJournalAdmin
- [ ] Remove `model_used` from AppJournalAdmin readonly_fields
- [ ] Change `model_used` → `ai_model_used` in ConversationAdmin
- [ ] Change `tokens_used` → `generation_tokens` in ConversationAdmin
- [ ] Change `rating` → `user_rating` in ConversationAdmin
- [ ] Check and fix `is_read` field in ConversationAdmin
- [ ] Remove `is_ai_generated` from ConversationAdmin list_filter
- [ ] Review/remove ConversationFeedbackAdmin if model doesn't exist
- [ ] Change `condition` → `conditions` in ConversationTriggerAdmin
- [ ] Remove `created_at` from ConversationTriggerAdmin
- [ ] Change `is_ai_generated` → `ai_generated` in DeviceJournalAdmin
- [ ] Remove `model_used` from DeviceJournalAdmin readonly_fields

---

## Recommended Approach

1. **Check each model file** to verify actual field names
2. **Update admin.py files** to match model field names exactly
3. **Test with:** `python manage.py check`
4. **Run migrations once all errors are fixed:** `python manage.py makemigrations`

---

## Model Reference Files

To verify field names, check these files:

- `server/apps/applications/models.py` - for App, AppRelationship, DeviceApp
- `server/apps/conversations/models.py` - for all Conversation-related models
- Other model files in respective app folders

---

## Additional Notes

- The errors are **admin configuration mismatches**, not database issues
- All models exist, just field names in admin.py are incorrect
- This likely happened because admin.py was written before final model structure
- After fixing admin errors, you may still need to address the PostgreSQL version requirement (currently requires 14+, you have 12.22)

