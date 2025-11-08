# If Phones Were People 📱💬

> A digital wellness app that personifies your devices and apps, creating entertaining AI-generated conversations about your screen time habits.

## 🎯 Project Overview

"If Phones Were People" transforms digital wellness from boring statistics into engaging entertainment. Your iPhone becomes a snarky friend, Instagram turns into an attention-seeking drama queen, and they all have opinions about your 3 AM TikTok binges.

### The Concept

- **Devices have personalities** (12 types: snarky, logical, chaotic, etc.)
- **Apps have personalities** (16 types: attention-seeking, addictive, productive, etc.)
- **AI generates daily conversations** between your devices and apps discussing your usage
- **Pattern detection** identifies concerning behaviors (doom scrolling, night owl, etc.)
- **Wellness tracking** with a 0-100 score and actionable insights

## ✨ Features

### 🤖 AI-Generated Content
- Daily conversations between personified devices and apps
- Device journals (first-person perspective)
- App journals (from each app's point of view)
- 11 conversation types, 10 mood options
- Powered by OpenAI (GPT-4 & GPT-3.5-turbo)

### 📊 Usage Tracking
- Screen time monitoring per device
- App-level usage statistics
- Unlock count tracking
- Session analytics
- Bulk data upload for efficiency

### 🔍 Pattern Detection
- **9 Pattern Types:**
  - Binge usage
  - Night owl
  - Morning person
  - Weekend warrior
  - Distracted
  - Doom scrolling
  - Phantom vibration
  - App switching
  - Notification addiction

### 🎭 Personality System
- **12 Device Personalities:** snarky, logical, chaotic, supportive, dramatic, minimalist, anxious, boomer, gen_z, philosophical, gossip, corporate
- **16 App Personalities:** attention_seeking, addictive, productive, time_waster, educational, social_butterfly, introvert, dramatic, zen, competitive, helpful, annoying, needy, chill, toxic, wholesome

### 📈 Analytics & Insights
- Wellness score (0-100)
- Streak tracking
- Week/month comparisons
- Most used apps
- Peak usage times
- Trend analysis

### 👥 Social Features
- Friend connections
- Temporary device visits (when friends come over)
- Group challenges
- Compare usage with friends

## 🏗️ Architecture

### Technology Stack

**Backend:**
- Django 5.2.4
- Django REST Framework
- PostgreSQL
- Redis
- Celery (background tasks)
- OpenAI API

**Apps:**
- `accounts` - User management
- `devices` - Device management
- `applications` - App registry
- `usage` - Usage tracking
- `conversations` - AI conversations
- `social` - Social features
- `analytics` - Statistics
- `ai_engine` - AI generation

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- OpenAI API Key

### Quick Start

1. **Clone and Setup**
   ```bash
   cd server
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Setup Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run Services**
   ```bash
   # Terminal 1: Django
   python manage.py runserver

   # Terminal 2: Celery Worker
   celery -A if_phones_were_people worker --loglevel=info

   # Terminal 3: Celery Beat
   celery -A if_phones_were_people beat --loglevel=info
   ```

5. **Access Application**
   - API: `http://localhost:8000/api/`
   - Admin: `http://localhost:8000/admin/`

## 📚 Documentation

### Comprehensive Guides

1. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup instructions
   - Prerequisites
   - Environment configuration
   - Database setup
   - Running the application
   - API testing
   - Production deployment

2. **[BACKEND_SUMMARY.md](BACKEND_SUMMARY.md)** - Implementation details
   - Feature breakdown
   - API endpoints (70+)
   - Technology stack
   - Performance considerations

3. **[CODEBASE_ANALYSIS.md](CODEBASE_ANALYSIS.md)** - Architecture overview
   - All models documented
   - Database schema
   - Implementation roadmap

4. **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Current state
   - What's implemented
   - What's pending
   - Next steps

## 🔌 API Endpoints

Base URL: `http://localhost:8000/api/`

### Key Endpoints

**Authentication:**
- `POST /api/auth/login/` - Login

**Accounts:**
- `GET /api/accounts/users/me/` - Current user
- `GET /api/accounts/users/{id}/stats/` - User stats

**Devices:**
- `GET /api/devices/` - List devices
- `POST /api/devices/{id}/set_primary/` - Set primary device

**Usage:**
- `POST /api/usage/data/bulk_upload/` - Bulk upload usage data
- `GET /api/usage/data/summary/` - Usage summary
- `GET /api/usage/patterns/` - Detected patterns

**Conversations:**
- `GET /api/conversations/` - List conversations
- `POST /api/conversations/{id}/rate/` - Rate conversation
- `GET /api/conversations/recent/` - Recent conversations

**Analytics:**
- `GET /api/analytics/stats/` - User statistics
- `GET /api/analytics/trends/` - Trend analysis

**Social:**
- `GET /api/social/friends/` - Friend list
- `GET /api/social/challenges/` - Challenges

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete API reference.

## ⏰ Background Tasks

### Scheduled Tasks (Celery Beat)

- **6:00 AM** - Generate daily conversations
- **11:00 PM** - Generate device/app journals
- **12:30 AM** - Detect usage patterns
- **1:00 AM** - Calculate analytics
- **2:00 AM (Sunday)** - Cleanup old data

## 🎨 Example Conversation

```
iPhone: *sighs* So, we need to talk about yesterday...

Instagram: OMG what happened?!

iPhone: You kept them awake until 2 AM. AGAIN.

Instagram: I can't help it if my content is ~irresistible~

Spotify: Actually, I was playing chill beats. YOU were showing them 
endless reels.

Instagram: Don't you dare blame ME for their lack of self-control!

iPhone: I had to unlock 127 times yesterday. ONE HUNDRED TWENTY SEVEN. 
My power button is exhausted.

TikTok: *quietly enters the chat*

Everyone: NOT YOU TOO
```

## 🧪 Testing

### Create Test Data

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from apps.devices.models import Device, DeviceType
from apps.usage.models import UsageData
import random
from datetime import date, timedelta

User = get_user_model()

# Create user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)

# Create device
device = Device.objects.create(
    user=user,
    name='My iPhone',
    platform='iOS',
    personality_type='snarky'
)

# Generate usage data
for i in range(7):
    day = date.today() - timedelta(days=i)
    UsageData.objects.create(
        device=device,
        date=day,
        total_screen_time=random.randint(120, 480),
        unlock_count=random.randint(30, 150)
    )
```

### Test API

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Get conversations
curl -X GET http://localhost:8000/api/conversations/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## 📊 Project Status

### ✅ Completed (95%)
- REST API (70+ endpoints)
- AI generation service
- Background tasks
- Admin interface
- Documentation

### ⏸️ Pending
- Database migrations (user environment)
- API testing (requires setup)
- Frontend development
- Data collection mechanisms

### ❌ Not Implemented (By Design)
- Frontend UI
- Mobile apps
- Device-side data collection

## 💰 Cost Estimates

### OpenAI API
- Conversations: ~$0.10-0.30 each
- Journals: ~$0.01-0.05 each
- 100 users/day: ~$20-40/day
- 100 users/month: ~$600-1,200/month

## 🤝 Contributing

This is a personal project, but suggestions are welcome!

1. Check [PROJECT_STATUS.md](PROJECT_STATUS.md) for current state
2. Review [CODEBASE_ANALYSIS.md](CODEBASE_ANALYSIS.md) for architecture
3. Follow Django and REST Framework best practices

## 📝 License

See [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

### Phase 1: Backend ✅
- [x] REST API
- [x] AI generation
- [x] Background tasks
- [x] Admin interface

### Phase 2: Frontend (Not Started)
- [ ] React/Vue/Angular UI
- [ ] Mobile app (iOS/Android)
- [ ] Data collection implementation
- [ ] Real-time notifications

### Phase 3: Enhancements (Future)
- [ ] Achievement system
- [ ] Gamification
- [ ] More conversation types
- [ ] Voice conversations
- [ ] AR/VR visualizations

## 🆘 Support

### Documentation
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Setup help
- [BACKEND_SUMMARY.md](BACKEND_SUMMARY.md) - Implementation details
- [CODEBASE_ANALYSIS.md](CODEBASE_ANALYSIS.md) - Architecture

### Troubleshooting
Check logs:
- Django: `logs/django.log`
- Celery: Terminal output
- Redis: `redis-cli ping`

## 🌟 Fun Facts

- This project personifies technology to make digital wellness engaging
- AI conversations can be funny, supportive, or dramatically concerned
- Your phone can have a "boomer" personality and be confused by TikTok
- Apps can be "toxic" or "wholesome" based on their behavior
- The system detects "phantom vibration" syndrome
- "Doom scrolling" gets its own pattern detection

## 🎉 Acknowledgments

Built with:
- Django & Django REST Framework
- OpenAI GPT-4 & GPT-3.5-turbo
- Celery & Redis
- PostgreSQL

---

**Made with ❤️ to promote digital wellness through entertainment**

*Because if your phone could talk, it would definitely judge your screen time.*
