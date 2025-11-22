# Seed Data Documentation

This document describes the initial seed data populated by the `seed_data` management command.

## Overview

The seed data management command populates the database with essential reference data needed for the application to function properly. This includes device types, personality traits, app categories, popular apps, and conversation triggers.

## Usage

### Basic Usage
```bash
python manage.py seed_data
```

### Reset and Recreate
```bash
python manage.py seed_data --reset
```

**⚠️ Warning**: The `--reset` flag will delete all existing seed data before creating new data. This will not affect user-generated data (devices, usage data, conversations, etc.), but will remove all apps, categories, device types, personality traits, and triggers.

## Data Created

### 1. Device Types (5 items)

Predefined device types with default personalities:

| Name | Icon | Platform Category | Default Personality |
|------|------|-------------------|---------------------|
| Smartphone | 📱 | mobile | social |
| Tablet | 📱 | tablet | chill |
| Laptop | 💻 | desktop | workaholic |
| Desktop | 🖥️ | desktop | logical |
| Smartwatch | ⌚ | wearable | anxious |

### 2. Personality Traits (16 items)

Personality traits organized by category:

#### Temperament
- **Snarky**: Quick-witted and sarcastic, loves making clever remarks
- **Logical**: Rational, analytical, and facts-focused
- **Chaotic**: Unpredictable, energetic, and all over the place
- **Supportive**: Encouraging, empathetic, and nurturing
- **Dramatic**: Theatrical, expressive, and loves attention
- **Minimalist**: Concise, straightforward, and no-nonsense

#### Humor Style
- **Witty**: Clever and quick with jokes
- **Self-Deprecating**: Makes jokes at own expense

#### Communication Style
- **Verbose**: Uses many words, loves detail
- **Concise**: Brief and to the point

#### Attitude
- **Optimistic**: Positive outlook, sees the bright side
- **Pessimistic**: Expects the worst, skeptical
- **Competitive**: Driven to win and compare

#### Quirks
- **Anxious**: Worried, overthinking everything
- **Gossipy**: Loves sharing information about others
- **Philosophical**: Contemplative, asks deep questions

#### Trait Relationships

The command also sets up compatibility and conflict relationships between traits:

**Compatible Pairs:**
- Snarky ↔ Witty, Self-Deprecating, Pessimistic
- Logical ↔ Concise, Minimalist
- Chaotic ↔ Dramatic, Gossipy, Verbose
- Supportive ↔ Optimistic, Verbose

**Conflicting Pairs:**
- Snarky ↔ Supportive, Optimistic
- Logical ↔ Chaotic, Dramatic
- Chaotic ↔ Minimalist, Concise
- Supportive ↔ Snarky, Pessimistic

### 3. App Categories (10 items)

| Name | Icon | Color | Default Personality Traits |
|------|------|-------|---------------------------|
| Social Media | 👥 | Blue (#3B82F6) | attention_seeking, social, addictive |
| Entertainment | 🎬 | Red (#EF4444) | entertaining, addictive, chill |
| Productivity | ✅ | Green (#10B981) | workaholic, productive, helpful |
| News | 📰 | Orange (#F59E0B) | dramatic, gossip, attention_seeking |
| Shopping | 🛍️ | Pink (#EC4899) | attention_seeking, chaotic, addictive |
| Health & Fitness | 💪 | Teal (#14B8A6) | helpful, competitive, productive |
| Education | 📚 | Purple (#8B5CF6) | educational, helpful, productive |
| Finance | 💰 | Dark Green (#059669) | analytical, helpful, minimalist |
| Communication | 💬 | Cyan (#06B6D4) | social, helpful, workaholic |
| Utilities | 🔧 | Gray (#6B7280) | minimalist, helpful, chill |

### 4. Popular Apps (13 items)

#### Social Media
- **Instagram**: Obsessed with aesthetics and engagement (Addictive: 9/10, Productive: 2/10)
- **Twitter/X**: Drama queen, lives for hot takes (Addictive: 8/10, Productive: 3/10)

#### Entertainment
- **TikTok**: The endless scroll master (Addictive: 10/10, Productive: 1/10)
- **YouTube**: Your enabler for "just one more video" (Addictive: 9/10, Productive: 2/10)
- **Spotify**: Laid-back music curator (Addictive: 6/10, Productive: 5/10)
- **Netflix**: Master of "Are you still watching?" (Addictive: 9/10, Productive: 1/10)

#### Communication
- **WhatsApp**: The gossip central (Addictive: 7/10, Productive: 5/10)
- **Gmail**: Stressed workaholic (Addictive: 6/10, Productive: 8/10)

#### Productivity
- **Slack**: Corporate taskmaster (Addictive: 7/10, Productive: 7/10)
- **Notion**: Organized perfectionist (Addictive: 5/10, Productive: 9/10)

#### Shopping
- **Amazon**: Temptation incarnate (Addictive: 8/10, Productive: 3/10)

#### Health & Fitness
- **Strava**: Fitness zealot (Addictive: 5/10, Productive: 8/10)

#### Finance
- **PayPal**: Serious money manager (Addictive: 3/10, Productive: 7/10)

Each app includes:
- Bundle IDs for iOS and Android
- Primary brand color
- Default personality type
- Personality description
- Usage characteristics (session length, addictive potential, productivity score)
- Category flags (social media, entertainment, productivity, etc.)

### 5. Conversation Triggers (12 items)

#### Usage-Based Triggers
- **Daily Usage Recap** (Priority: 7, Cooldown: 24h)
  - End of day summary with 30+ minutes usage
  
- **Excessive App Usage** (Priority: 9, Cooldown: 12h)
  - Single app used for 120+ minutes in 4 hours
  
- **Screen Time Milestone** (Priority: 6, Cooldown: 6h)
  - Reaching 1, 2, 3, 4, 5, or 6 hour milestones

#### Pattern Detection Triggers
- **Late Night Scrolling** (Priority: 8, Cooldown: 24h)
  - Social media/entertainment between 11 PM - 3 AM for 30+ minutes
  
- **App Opening Spree** (Priority: 7, Cooldown: 12h)
  - 10+ app switches in 5 minutes
  
- **Productivity Streak** (Priority: 5, Cooldown: 24h)
  - 60%+ productivity apps for 120+ minutes
  
- **Social Media Marathon** (Priority: 8, Cooldown: 24h)
  - 180+ minutes social media in 24 hours
  
- **App Jealousy** (Priority: 4, Cooldown: 72h)
  - App usage dropped by 50%+ compared to last 7 days
  
- **Weekend Behavior Change** (Priority: 5, Cooldown: 168h)
  - 30%+ usage change on weekends

#### Time-Based Triggers
- **Morning Routine** (Priority: 6, Cooldown: 24h)
  - First apps checked between 6 AM - 9 AM

#### Social Event Triggers
- **Friend Device Visit** (Priority: 6, Cooldown: 48h)
  - Friend's device connected nearby

#### Goal Progress Triggers
- **Goal Progress Check** (Priority: 5, Cooldown: 168h)
  - Weekly review of active goals

## Idempotency

The command is idempotent, meaning it's safe to run multiple times. It uses `get_or_create()` for all objects:
- If an object already exists (based on unique fields), it will be skipped
- If an object doesn't exist, it will be created
- The command will report which objects were created vs. already existed

## Dependencies

The seed data is created in dependency order:
1. Device Types (no dependencies)
2. Personality Traits (no dependencies, then relationships set up)
3. App Categories (no dependencies)
4. Apps (depends on App Categories)
5. Conversation Triggers (no dependencies)

## Testing

After running the seed command, you can verify the data was created:

```bash
# Check counts
python manage.py shell
>>> from apps.devices.models import DeviceType, PersonalityTrait
>>> from apps.applications.models import AppCategory, App
>>> from apps.conversations.models import ConversationTrigger
>>> 
>>> DeviceType.objects.count()  # Should be 5
>>> PersonalityTrait.objects.count()  # Should be 16
>>> AppCategory.objects.count()  # Should be 10
>>> App.objects.count()  # Should be 13
>>> ConversationTrigger.objects.count()  # Should be 12
```

## Customization

To customize the seed data:
1. Edit `server/apps/devices/management/commands/seed_data.py`
2. Modify the data dictionaries in the relevant methods:
   - `create_device_types()`
   - `create_personality_traits()`
   - `create_app_categories()`
   - `create_apps()`
   - `create_conversation_triggers()`
3. Run the command with `--reset` to recreate with new data

## Notes

- All speech patterns and personality characteristics are stored as JSON for flexibility
- App bundle IDs should match actual app identifiers for proper tracking
- Personality traits include detailed speech pattern configurations for AI conversation generation
- Conversation triggers use JSON conditions for maximum flexibility
- Colors use hex format for consistent UI rendering
