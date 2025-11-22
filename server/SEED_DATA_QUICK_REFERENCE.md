# Seed Data Quick Reference

## Command Usage

### Run Seed Data
```bash
python manage.py seed_data
```

### Reset and Recreate
```bash
python manage.py seed_data --reset
```

## What Gets Created

### ✅ 5 Device Types
- Smartphone (📱 mobile, social)
- Tablet (📱 tablet, chill)
- Laptop (💻 desktop, workaholic)
- Desktop (🖥️ desktop, logical)
- Smartwatch (⌚ wearable, anxious)

### ✅ 16 Personality Traits
**Temperament:** Snarky, Logical, Chaotic, Supportive, Dramatic, Minimalist  
**Humor:** Witty, Self-Deprecating  
**Communication:** Verbose, Concise  
**Attitude:** Optimistic, Pessimistic, Competitive  
**Quirks:** Anxious, Gossipy, Philosophical

### ✅ 10 App Categories
Social Media • Entertainment • Productivity • News • Shopping  
Health & Fitness • Education • Finance • Communication • Utilities

### ✅ 13 Popular Apps
Instagram • TikTok • Twitter/X • WhatsApp • Gmail • Slack  
Notion • YouTube • Spotify • Netflix • Amazon • Strava • PayPal

### ✅ 12 Conversation Triggers
Daily Usage Recap • Excessive App Usage • Late Night Scrolling  
Screen Time Milestone • App Opening Spree • Productivity Streak  
Social Media Marathon • Friend Device Visit • Goal Progress Check  
App Jealousy • Weekend Behavior Change • Morning Routine

## Verification

Check data was created:
```bash
python manage.py shell -c "
from apps.devices.models import DeviceType, PersonalityTrait
from apps.applications.models import AppCategory, App
from apps.conversations.models import ConversationTrigger

print(f'Device Types: {DeviceType.objects.count()}')
print(f'Personality Traits: {PersonalityTrait.objects.count()}')
print(f'App Categories: {AppCategory.objects.count()}')
print(f'Apps: {App.objects.count()}')
print(f'Conversation Triggers: {ConversationTrigger.objects.count()}')
"
```

Expected output:
```
Device Types: 5
Personality Traits: 16
App Categories: 10
Apps: 13
Conversation Triggers: 12
```

## Features

✅ **Idempotent** - Safe to run multiple times  
✅ **Transactional** - All-or-nothing execution  
✅ **Verbose Output** - See what's being created  
✅ **Reset Option** - Clear and recreate data  

## Next Steps

After running seed data:
1. Run migrations for JWT token blacklist: `python manage.py migrate`
2. Create a superuser: `python manage.py createsuperuser`
3. Start the development server: `python manage.py runserver`
4. Access admin panel: http://localhost:8000/admin
5. Test API endpoints with Postman collection

## Notes

- Seed data includes realistic app personalities and usage metrics
- Personality traits have compatibility/conflict relationships
- Conversation triggers cover common usage patterns
- All data includes proper categorization and metadata
