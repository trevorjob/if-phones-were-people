# System Architecture Diagram

## Overall System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                            USER DEVICES                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│  │   iPhone    │  │   MacBook   │  │    iPad     │                 │
│  │  (Primary)  │  │             │  │             │                 │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                │
│         │                 │                 │                        │
│    Screen Time       Usage Stats       App Usage                    │
│         │                 │                 │                        │
└─────────┼─────────────────┼─────────────────┼────────────────────────┘
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
                   Data Collection Layer
                            │
          ┌─────────────────▼─────────────────┐
          │   iOS Shortcuts / Android Service  │
          │   - Collects screen time data      │
          │   - Formats into JSON              │
          │   - POSTs to backend API           │
          └─────────────────┬─────────────────┘
                            │
                            │ HTTPS POST
                            │
          ┌─────────────────▼─────────────────┐
          │      DJANGO REST API LAYER        │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │  Authentication & User Mgmt  │ │
          │  │  - Register / Login          │ │
          │  │  - Profile Management        │ │
          │  │  - API Key Generation        │ │
          │  └──────────────────────────────┘ │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │  Device Management           │ │
          │  │  - CRUD devices              │ │
          │  │  - Set personalities         │ │
          │  │  - Manage relationships      │ │
          │  └──────────────────────────────┘ │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │  App Management              │ │
          │  │  - Register installed apps   │ │
          │  │  - Set app personalities     │ │
          │  │  - Track app relationships   │ │
          │  └──────────────────────────────┘ │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │  Usage Data Ingestion        │ │
          │  │  - Receive usage data        │ │
          │  │  - Validate and store        │ │
          │  │  - Trigger pattern detection │ │
          │  └──────────────────────────────┘ │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │  Conversation API            │ │
          │  │  - List conversations        │ │
          │  │  - Get conversation details  │ │
          │  │  - Rate conversations        │ │
          │  └──────────────────────────────┘ │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │  Social Features API         │ │
          │  │  - Friend connections        │ │
          │  │  - Device visits             │ │
          │  │  - Challenges                │ │
          │  └──────────────────────────────┘ │
          └─────────────────┬─────────────────┘
                            │
                            │ Stores in
                            │
          ┌─────────────────▼─────────────────┐
          │      POSTGRESQL DATABASE          │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │ Users & Profiles             │ │
          │  └──────────────────────────────┘ │
          │  ┌──────────────────────────────┐ │
          │  │ Devices (with personalities) │ │
          │  └──────────────────────────────┘ │
          │  ┌──────────────────────────────┐ │
          │  │ Apps (with personalities)    │ │
          │  └──────────────────────────────┘ │
          │  ┌──────────────────────────────┐ │
          │  │ Usage Data (daily metrics)   │ │
          │  └──────────────────────────────┘ │
          │  ┌──────────────────────────────┐ │
          │  │ Conversations (AI-generated) │ │
          │  └──────────────────────────────┘ │
          │  ┌──────────────────────────────┐ │
          │  │ Patterns & Analytics         │ │
          │  └──────────────────────────────┘ │
          │  ┌──────────────────────────────┐ │
          │  │ Social Connections           │ │
          │  └──────────────────────────────┘ │
          └─────────────────┬─────────────────┘
                            │
          ┌─────────────────▼─────────────────┐
          │         CELERY WORKER             │
          │      (Background Processing)      │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │ Daily Tasks (6 AM)           │ │
          │  │ - Check usage data           │ │
          │  │ - Detect patterns            │ │
          │  │ - Evaluate triggers          │ │
          │  │ - Generate conversations     │ │
          │  └──────────────────────────────┘ │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │ Pattern Detection            │ │
          │  │ - Analyze usage trends       │ │
          │  │ - Identify habits            │ │
          │  │ - Calculate streaks          │ │
          │  └──────────────────────────────┘ │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │ Analytics Processing         │ │
          │  │ - Aggregate statistics       │ │
          │  │ - Generate insights          │ │
          │  │ - Compare with friends       │ │
          │  └──────────────────────────────┘ │
          └─────────────────┬─────────────────┘
                            │
                   Calls when needed
                            │
          ┌─────────────────▼─────────────────┐
          │         AI ENGINE                 │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │ OpenAI GPT-4 / Anthropic     │ │
          │  │                               │ │
          │  │  Input:                       │ │
          │  │  - Device personalities       │ │
          │  │  - App personalities          │ │
          │  │  - Usage data                 │ │
          │  │  - Detected patterns          │ │
          │  │  - Relationships              │ │
          │  │                               │ │
          │  │  Output:                      │ │
          │  │  - Entertaining conversation  │ │
          │  │  - Device journal entry       │ │
          │  │  - App journal entry          │ │
          │  └──────────────────────────────┘ │
          └───────────────────────────────────┘
                            │
                  Conversation saved
                            │
          ┌─────────────────▼─────────────────┐
          │   NOTIFICATION SYSTEM             │
          │   - Email notifications           │
          │   - Push notifications (future)   │
          │   - In-app notifications          │
          └─────────────────┬─────────────────┘
                            │
          ┌─────────────────▼─────────────────┐
          │         WEB/MOBILE APP            │
          │         (FRONTEND - TBD)          │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │ Dashboard                     │ │
          │  │ - Today's conversation        │ │
          │  │ - Usage summary               │ │
          │  │ - Quick stats                 │ │
          │  └──────────────────────────────┘ │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │ Conversation Feed             │ │
          │  │ - Browse past conversations   │ │
          │  │ - Rate conversations          │ │
          │  │ - Mark favorites              │ │
          │  └──────────────────────────────┘ │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │ Device Manager                │ │
          │  │ - Add/edit devices            │ │
          │  │ - Customize personalities     │ │
          │  │ - Set relationships           │ │
          │  └──────────────────────────────┘ │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │ Analytics Dashboard           │ │
          │  │ - Usage trends                │ │
          │  │ - Pattern insights            │ │
          │  │ - Goal tracking               │ │
          │  └──────────────────────────────┘ │
          │                                    │
          │  ┌──────────────────────────────┐ │
          │  │ Social Hub                    │ │
          │  │ - Friend connections          │ │
          │  │ - Challenges                  │ │
          │  │ - Leaderboards                │ │
          │  └──────────────────────────────┘ │
          └───────────────────────────────────┘
```

## Data Flow Example: Daily Conversation Generation

```
1. USER DEVICE (iPhone)
   └─> iOS Shortcuts runs at 11:59 PM
       └─> Collects today's Screen Time data
           - Total screen time: 4h 32m
           - Instagram: 2h 15m
           - Twitter: 45m
           - Safari: 1h 10m
           - Other apps...
       
2. DATA COLLECTION
   └─> Shortcuts formats data as JSON
       └─> POSTs to: /api/usage/data/bulk_upload/
           {
             "device_id": "uuid-of-iphone",
             "date": "2025-11-06",
             "total_screen_time": 272,
             "apps": [...]
           }

3. BACKEND API
   └─> Receives and validates data
       └─> Stores in UsageData model
           └─> Triggers pattern detection
               - Detects: "Social media spiral" pattern
               - Instagram usage up 50% vs average

4. CELERY BEAT (6 AM next day)
   └─> Scheduled task runs: generate_daily_conversations()
       └─> Queries yesterday's usage data
       └─> Evaluates conversation triggers
           ✓ Usage threshold exceeded (4+ hours)
           ✓ Pattern detected (social media spiral)
       └─> Prepares conversation context:
           Devices: [iPhone (Snarky personality)]
           Apps: [Instagram (Addictive), Twitter (Chaotic)]
           Usage: [4h32m total, Instagram dominant]
           Pattern: [Social media spiral]

5. AI ENGINE
   └─> Builds personality-aware prompt:
       """
       You're creating a conversation between:
       - iPhone (snarky personality, judges usage)
       - Instagram (addictive, attention-seeking)
       - Twitter (chaotic, dramatic)
       
       Yesterday's usage:
       - Total: 4h 32m (heavy usage day)
       - Instagram: 2h 15m (50% increase)
       - Detected pattern: Social media spiral
       
       Create a humorous 300-word conversation where
       iPhone roasts the user's Instagram addiction
       while Instagram and Twitter argue about who's
       more addictive. Make it entertaining but insightful.
       """
   
   └─> Calls OpenAI GPT-4
       └─> Receives generated conversation:
           
           iPhone: *sighs dramatically* So... we need to talk about yesterday.
           
           Instagram: OMG what?! Did you see how many reels we watched?! 
           
           Twitter: Wait, I was there too! Remember that 3 AM doomscroll session?
           
           iPhone: Exactly. 4 hours and 32 minutes. TWO HOURS on Instagram alone.
           
           Instagram: And every minute was BEAUTIFUL! Those cooking videos, 
           the travel content, the memes—
           
           Twitter: Please, MY chaos is way more engaging.
           
           iPhone: You're both terrible influences. We had plans! Remember 
           that book? The one we opened for exactly 4 minutes?
           
           Instagram: Books don't have infinite scroll though...
           
           [conversation continues...]

6. BACKEND PROCESSING
   └─> Saves Conversation to database
       - Links to devices & apps
       - Saves trigger data
       - Records AI generation cost
   
   └─> Triggers notification
       - Sends email: "Your devices had a chat about yesterday"
       - Push notification (if app installed)

7. USER SEES IT
   └─> Opens app/email
       └─> Reads entertaining conversation
           └─> Laughs at accuracy
               └─> Realizes Instagram usage is high
                   └─> Sets usage goal
                       └─> Gets motivated to change

8. USER RATES IT
   └─> Gives 5-star rating
       └─> Feedback stored for AI improvement
           └─> Future conversations get better
```

## Personality System Flow

```
DEVICE PERSONALITY
├─ Base Type: "Snarky"
│  ├─ Speech patterns: Sarcastic, witty
│  ├─ Attitudes: Judgemental about usage
│  └─ Reactions: Eye-rolls, dramatic sighs
│
├─ Additional Traits: ["Workaholic", "Protective"]
│  ├─ Workaholic: Pushes for productivity
│  └─ Protective: Worries about screen time
│
└─ Custom Notes: "Extra sarcastic on weekends"

          ↓ Combined in AI prompt ↓

AI GENERATION PROMPT:
"This iPhone is snarky and judgemental, always making
witty comments about excessive phone usage. It's also
a workaholic who constantly pushes for more productivity,
and protective of the user's wellbeing. It gets extra
sarcastic on weekends when usage spikes."

          ↓ Produces ↓

GENERATED DIALOGUE:
iPhone: "Oh fantastic, another weekend where you spent
more time with Instagram than with actual humans. I'm
honored to be part of your thrilling doom-scroll marathon.
Really, that's exactly what I was built for."
```

## Database Relationships

```
User (1) ──────────┐
                   │
                   ├─ has many ──> Device (N)
                   │                   │
                   │                   ├─ has many ──> DeviceApp (N)
                   │                   │                   │
                   │                   │                   ├─ has many ──> AppUsage (N)
                   │                   │                   └─ has ──────> App (1)
                   │                   │
                   │                   ├─ has many ──> UsageData (N)
                   │                   └─ has many ──> DeviceJournal (N)
                   │
                   ├─ has many ──> Conversation (N)
                   │                   │
                   │                   ├─ references ──> Device (N) many-to-many
                   │                   ├─ references ──> DeviceApp (N) many-to-many
                   │                   └─ triggered by ─> ConversationTrigger (N)
                   │
                   ├─ has many ──> UsagePattern (N)
                   ├─ has many ──> UsageGoal (N)
                   └─ has many ──> FriendConnection (N)
                                       │
                                       └─ references ──> User (1)

Device (1) ───> has ───> DeviceRelationship (N) ───> references ───> Device (1)
   │
   └─> belongs to ───> DeviceType (1)
   └─> has many ───> PersonalityTrait (N) many-to-many

App (1) ───────> has ───> AppCategory (1)

DeviceApp (1) ──> has ───> AppRelationship (N) ───> references ───> DeviceApp (1)
```

## Technology Stack Visual

```
┌──────────────────────────────────────────────────┐
│                   FRONTEND                       │
│  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │   React    │  │   React    │  │  Flutter  │ │
│  │  Web App   │  │   Native   │  │ (future)  │ │
│  └────────────┘  └────────────┘  └───────────┘ │
└─────────────────┬────────────────────────────────┘
                  │ REST API (JSON)
┌─────────────────▼────────────────────────────────┐
│              API LAYER (Django)                  │
│  ┌──────────────────────────────────────────┐   │
│  │  Django REST Framework                    │   │
│  │  - Token Authentication                   │   │
│  │  - Serializers                            │   │
│  │  - ViewSets                               │   │
│  │  - Filtering & Pagination                 │   │
│  └──────────────────────────────────────────┘   │
└─────────────────┬────────────────────────────────┘
                  │
┌─────────────────▼────────────────────────────────┐
│           BUSINESS LOGIC (Django)                │
│  ┌──────────────────────────────────────────┐   │
│  │  Django Apps (8 total)                    │   │
│  │  - accounts (auth, profiles)              │   │
│  │  - devices (device management)            │   │
│  │  - applications (app management)          │   │
│  │  - usage (tracking & patterns)            │   │
│  │  - conversations (AI generation)          │   │
│  │  - social (friends & challenges)          │   │
│  │  - analytics (insights & trends)          │   │
│  │  - ai_engine (AI orchestration)           │   │
│  └──────────────────────────────────────────┘   │
└─────────────────┬────────────────────────────────┘
                  │
┌─────────────────▼────────────────────────────────┐
│              DATABASE LAYER                      │
│  ┌──────────────────────────────────────────┐   │
│  │  PostgreSQL 15+                           │   │
│  │  - Django ORM                             │   │
│  │  - JSON field support                     │   │
│  │  - Full-text search                       │   │
│  │  - Complex relationships                  │   │
│  └──────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│         BACKGROUND TASKS (Celery)                │
│  ┌──────────────────────────────────────────┐   │
│  │  Celery Workers                           │   │
│  │  - Conversation generation                │   │
│  │  - Pattern detection                      │   │
│  │  - Analytics calculation                  │   │
│  │  - Email notifications                    │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │  Celery Beat (Scheduler)                  │   │
│  │  - Daily tasks at 6 AM                    │   │
│  │  - Weekly analytics                       │   │
│  │  - Cleanup old data                       │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │  Redis                                    │   │
│  │  - Message broker                         │   │
│  │  - Result backend                         │   │
│  │  - Caching (future)                       │   │
│  └──────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│             AI SERVICES (External)               │
│  ┌──────────────────────────────────────────┐   │
│  │  OpenAI API                               │   │
│  │  - GPT-4 for conversations                │   │
│  │  - Primary AI provider                    │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │  Anthropic API                            │   │
│  │  - Claude as fallback                     │   │
│  │  - Backup AI provider                     │   │
│  └──────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```

This architecture provides:
- **Scalability**: Separate layers can scale independently
- **Maintainability**: Clean separation of concerns
- **Testability**: Each layer can be tested in isolation
- **Flexibility**: Easy to swap components (different AI, database, etc.)
