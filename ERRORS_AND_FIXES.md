# Critical Errors Found and Fixes

## 🔴 CRITICAL ISSUES

### 1. **Inconsistent Model Field Names**

**Error Locations:**
- `apps/usage/models.py` - Model is `AppUsage` but code references `AppUsageData`
- `apps/usage/tasks.py` line 12, 67, 232 - Uses `AppUsageData`
- `apps/ai_engine/tasks.py` line 12 - Imports `AppUsageData`

**Fix Required:**
```python
# In all files, change:
from apps.usage.models import AppUsageData  # WRONG
# To:
from apps.usage.models import AppUsage  # CORRECT

# Update all references from AppUsageData to AppUsage
```

---

### 2. **Missing/Incorrect Conversation Model Fields**

**Error Location:** `apps/ai_engine/tasks.py` lines 131-136

**Problem:**
```python
conversation = Conversation.objects.create(
    user=user,
    conversation_type=conversation_type,
    mood=mood,
    content=ai_result['content'],
    model_used=ai_result['model_used'],  # Field name mismatch
    generation_prompt=ai_result['generation_prompt'],
    tokens_used=ai_result['tokens_used'],  # Field name mismatch
    generation_cost=ai_result['cost'],
    is_ai_generated=True  # Field doesn't exist
)
```

**Actual Conversation Model Fields:**
- `ai_model_used` (not `model_used`)
- `generation_tokens` (not `tokens_used`)
- No `is_ai_generated` field exists

**Fix Required:**
```python
conversation = Conversation.objects.create(
    user=user,
    conversation_type=conversation_type,
    mood=mood,
    content=ai_result['content'],
    ai_model_used=ai_result['model_used'],  # CORRECT
    generation_prompt=ai_result['generation_prompt'],
    generation_tokens=ai_result['tokens_used'],  # CORRECT
    generation_cost=ai_result['cost'],
    generation_status='completed'  # Add status
)
```

---

### 3. **Missing UsagePattern Model Fields**

**Error Location:** `apps/usage/tasks.py` lines 77-89

**Problem:**
```python
UsagePattern.objects.get_or_create(
    user=user,
    pattern_type='binge_usage',
    defaults={
        'description': '...',
        'severity': 'medium',  # Field doesn't exist
        'confidence': 0.8,  # Should be confidence_score
        'metadata': {...}  # Should be pattern_data
    }
)
```

**Actual UsagePattern Model Fields:**
- `confidence_score` (not `confidence`)
- `pattern_data` (not `metadata`)
- No `severity` field (use `strength` instead)

**Fix Required:**
```python
UsagePattern.objects.get_or_create(
    user=user,
    pattern_type='binge_usage',
    defaults={
        'description': '...',
        'start_date': date,
        'frequency': 'daily',
        'strength': 'moderate',  # CORRECT
        'confidence_score': 0.8,  # CORRECT
        'pattern_data': {...}  # CORRECT
    }
)
```

---

### 4. **Missing Field: first_detected**

**Error Location:** `apps/ai_engine/tasks.py` line 98

**Problem:**
```python
patterns = UsagePattern.objects.filter(
    user=user,
    first_detected__date=date  # Field doesn't exist
)
```

**Fix Required:**
```python
patterns = UsagePattern.objects.filter(
    user=user,
    start_date=date  # CORRECT - use start_date
)
```

---

### 5. **Incorrect AppUsage Relationships**

**Error Location:** Multiple files

**Problem:**
- `AppUsage` model has relationship to `DeviceApp` via `device_app` field
- But code references wrong relationships like `app_usage__usage_data`

**Actual AppUsage Model:**
```python
class AppUsage(models.Model):
    device_app = models.ForeignKey('applications.DeviceApp', on_delete=models.CASCADE, related_name='usage_data')
    date = models.DateField()
    time_spent_minutes = models.IntegerField(default=0)
    # ... (not linked to UsageData directly)
```

**Fix Required:**
Update all queries to use correct relationships.

---

### 6. **Duplicate Celery Configuration in settings.py**

**Error Location:** `server/if_phones_were_people/settings.py` lines 194-200 and 260-268

**Problem:** Celery configuration defined twice, causing conflicts

**Status:** ✅ **FIXED** in previous update

---

### 7. **Incorrect STATICFILES_DIRS Configuration**

**Error Location:** `settings.py` line 155

**Problem:** References `BASE_DIR / 'static'` directory that may not exist

**Status:** ✅ **FIXED** (commented out)

---

### 8. **Missing django.db import in tasks**

**Error Location:** `apps/ai_engine/tasks.py` line 83

**Problem:**
```python
total_usage = UsageData.objects.filter(...).aggregate(
    total_time=models.Sum('total_screen_time'),  # models not imported
    total_unlocks=models.Sum('unlock_count')
)
```

**Fix Required:**
```python
# Add at top of file:
from django.db.models import Sum, Avg, Count, F, Q

# Then use:
total_time=Sum('total_screen_time'),
total_unlocks=Sum('unlock_count')
```

---

### 9. **DeviceJournal Fields Mismatch**

**Error Location:** `apps/ai_engine/tasks.py` lines 244-250

**Problem:**
```python
DeviceJournal.objects.create(
    device=device,
    date=date,
    content=ai_result['content'],
    mood='reflective',  # Not a valid choice
    model_used=ai_result['model_used'],  # Field doesn't exist
    generation_prompt=ai_result['generation_prompt'],
)
```

**Actual DeviceJournal mood choices:**
- 'happy', 'frustrated', 'proud', 'tired', 'excited', 'confused', 'satisfied', 'overwhelmed', 'bored', 'grateful'
- NO 'reflective' option

**Fix Required:**
```python
DeviceJournal.objects.create(
    device=device,
    date=date,
    content=ai_result['content'],
    mood='satisfied',  # CORRECT choice
    generation_prompt=ai_result['generation_prompt'],
    # Remove model_used - field doesn't exist
)
```

---

### 10. **Missing AppUsage Time Fields**

**Error Location:** Various tasks

**Problem:** Code references `time_spent` but model field is `time_spent_minutes`

**Fix Required:** Use `time_spent_minutes` everywhere

---

## 📝 FILES THAT NEED FIXING

1. ✅ `server/if_phones_were_people/settings.py` - FIXED
2. ❌ `server/apps/ai_engine/tasks.py` - NEEDS FIXES
3. ❌ `server/apps/usage/tasks.py` - NEEDS FIXES  
4. ❌ `server/apps/usage/models.py` - Clarify AppUsage vs AppUsageData
5. ❌ `server/apps/analytics/tasks.py` - Likely has similar issues

---

## 🔧 IMMEDIATE ACTION ITEMS

### Priority 1 (Blocking)
1. Fix AppUsageData → AppUsage naming throughout
2. Fix Conversation model field names
3. Fix UsagePattern field names
4. Add missing imports (django.db.models)

### Priority 2 (Important)
5. Fix DeviceJournal mood choices
6. Fix AppUsage query relationships
7. Validate all model field references

### Priority 3 (Nice to have)
8. Add comprehensive logging
9. Add error handling for missing data
10. Add data validation

---

## 🎯 NEXT STEPS

1. I'll now systematically fix all these issues
2. Each fix will be tested for syntax
3. Create a validation script to catch future issues
4. Update documentation with correct field names

---

*Generated: 2025-11-13*
