# Setup and Deployment Guide

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- OpenAI API Key

## Initial Setup

### 1. Environment Configuration

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and fill in the required values:

```env
# Database
DB_NAME=if_phones_were_people_db
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here

# App Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2. Create Virtual Environment

```bash
cd server
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Create PostgreSQL database:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE if_phones_were_people_db;

# Create user
CREATE USER your_db_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE if_phones_were_people_db TO your_db_user;

# Exit
\q
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow prompts to create admin account.

### 7. Load Initial Data (Optional)

You can load device types, app categories, and personality presets:

```bash
python manage.py shell
```

```python
from apps.devices.models import DeviceType, PersonalityTrait
from apps.applications.models import AppCategory

# Create device types
DeviceType.objects.create(
    name='Smartphone',
    description='Mobile smartphone device',
    icon='📱'
)
DeviceType.objects.create(
    name='Tablet',
    description='Tablet device',
    icon='📱'
)
DeviceType.objects.create(
    name='Laptop',
    description='Laptop computer',
    icon='💻'
)

# Create app categories
categories = [
    ('Social', 'Social media and messaging'),
    ('Entertainment', 'Video, music, and games'),
    ('Productivity', 'Work and productivity tools'),
    ('News', 'News and information'),
    ('Shopping', 'Shopping and e-commerce'),
    ('Health', 'Health and fitness'),
    ('Education', 'Learning and education'),
    ('Finance', 'Banking and finance'),
]

for name, desc in categories:
    AppCategory.objects.create(name=name, description=desc)

# Create personality traits
traits = [
    ('snarky', 'Snarky', 'Witty and sarcastic commentary'),
    ('logical', 'Logical', 'Analytical and data-driven'),
    ('chaotic', 'Chaotic', 'Unpredictable and wild'),
    ('supportive', 'Supportive', 'Encouraging and positive'),
    ('dramatic', 'Dramatic', 'Over-the-top emotional responses'),
    ('minimalist', 'Minimalist', 'Calm and focused on essentials'),
    ('anxious', 'Anxious', 'Worried about everything'),
    ('boomer', 'Boomer', 'Confused by modern tech'),
    ('gen_z', 'Gen Z', 'Extremely online and memey'),
    ('philosophical', 'Philosophical', 'Deep and contemplative'),
    ('gossip', 'Gossip', 'Lives for the drama and tea'),
    ('corporate', 'Corporate', 'Professional buzzword speaker'),
]

for code, name, desc in traits:
    PersonalityTrait.objects.create(
        trait_code=code,
        trait_name=name,
        description=desc
    )

exit()
```

## Running the Application

### Start Development Server

```bash
python manage.py runserver
```

Application will be available at: `http://localhost:8000`
API endpoints: `http://localhost:8000/api/`
Admin panel: `http://localhost:8000/admin/`

### Start Celery Worker

In a new terminal (with venv activated):

```bash
celery -A if_phones_were_people worker --loglevel=info
```

### Start Celery Beat (Scheduler)

In another new terminal (with venv activated):

```bash
celery -A if_phones_were_people beat --loglevel=info
```

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout

### Accounts
- `GET /api/accounts/users/` - List users
- `GET /api/accounts/users/me/` - Get current user
- `POST /api/accounts/users/` - Register new user
- `GET /api/accounts/users/{id}/stats/` - Get user stats
- `POST /api/accounts/users/{id}/change_password/` - Change password
- `GET /api/accounts/profiles/` - List profiles
- `GET/PUT /api/accounts/profiles/{id}/` - Profile detail/update

### Devices
- `GET /api/devices/` - List devices
- `POST /api/devices/` - Create device
- `GET /api/devices/{id}/` - Device detail
- `PUT /api/devices/{id}/` - Update device
- `DELETE /api/devices/{id}/` - Delete device
- `POST /api/devices/{id}/set_primary/` - Set as primary device
- `POST /api/devices/{id}/sync/` - Sync device data

### Applications
- `GET /api/apps/registry/` - List all available apps
- `GET /api/apps/device-apps/` - List user's device apps
- `POST /api/apps/device-apps/` - Add app to device
- `GET /api/apps/device-apps/{id}/` - Device app detail
- `PUT /api/apps/device-apps/{id}/` - Update device app
- `DELETE /api/apps/device-apps/{id}/` - Remove app

### Usage
- `GET /api/usage/data/` - List usage data
- `POST /api/usage/data/` - Create usage entry
- `POST /api/usage/data/bulk_upload/` - Bulk upload usage data
- `GET /api/usage/data/summary/` - Get usage summary
- `GET /api/usage/data/top_apps/` - Get top apps
- `GET /api/usage/patterns/` - List detected patterns
- `GET /api/usage/goals/` - List goals
- `POST /api/usage/goals/` - Create goal

### Conversations
- `GET /api/conversations/` - List conversations
- `GET /api/conversations/{id}/` - Conversation detail
- `POST /api/conversations/{id}/rate/` - Rate conversation
- `POST /api/conversations/{id}/toggle_favorite/` - Toggle favorite
- `GET /api/conversations/recent/` - Get recent conversations
- `GET /api/conversations/device-journals/` - Device journals
- `GET /api/conversations/app-journals/` - App journals

### Social
- `GET /api/social/friends/` - List friend connections
- `POST /api/social/friends/` - Send friend request
- `GET /api/social/challenges/` - List challenges
- `POST /api/social/challenges/` - Create challenge
- `POST /api/social/challenges/{id}/join/` - Join challenge
- `POST /api/social/challenges/{id}/leave/` - Leave challenge

### Analytics
- `GET /api/analytics/stats/` - User statistics
- `GET /api/analytics/stats/{id}/` - Specific user stats
- `GET /api/analytics/trends/` - Trend analysis

## Testing with Sample Data

### Create Test User

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile
from apps.devices.models import Device, DeviceType
from apps.applications.models import App, DeviceApp, AppCategory

User = get_user_model()

# Create test user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)

# Create profile
UserProfile.objects.create(
    user=user,
    timezone='America/New_York',
    preferred_conversation_time='18:00:00'
)

# Create device
device_type = DeviceType.objects.first()
device = Device.objects.create(
    user=user,
    name='My iPhone',
    platform='iOS',
    device_type=device_type,
    is_primary=True,
    personality_type='snarky'
)

# Create apps
social_cat = AppCategory.objects.get(name='Social')
instagram = App.objects.create(
    name='Instagram',
    bundle_id='com.instagram.instagram',
    category=social_cat,
    default_personality='attention_seeking'
)

# Add app to device
DeviceApp.objects.create(
    device=device,
    app=instagram,
    custom_name='Insta',
    is_installed=True
)

print(f"Created test user: {user.username}")
print(f"Created device: {device.name}")
print(f"Created app: {instagram.name}")
```

### Generate Test Usage Data

```python
from apps.usage.models import UsageData, AppUsageData
from datetime import date, timedelta
import random

# Generate usage for last 7 days
for i in range(7):
    day = date.today() - timedelta(days=i)
    
    usage = UsageData.objects.create(
        device=device,
        date=day,
        total_screen_time=random.randint(120, 480),  # 2-8 hours
        unlock_count=random.randint(30, 150)
    )
    
    # Add app usage
    device_app = device.device_apps.first()
    if device_app:
        AppUsageData.objects.create(
            usage_data=usage,
            device_app=device_app,
            time_spent=random.randint(30, 180),  # 30min - 3hrs
            launch_count=random.randint(5, 30)
        )

print("Generated 7 days of usage data")
```

### Trigger Conversation Generation

```python
from apps.ai_engine.tasks import generate_conversation_on_demand

# Generate conversation for test user
result = generate_conversation_on_demand.delay(user.id)
print(f"Triggered conversation generation: {result.id}")

# Check result after a few seconds
print(result.get(timeout=30))
```

## Production Deployment

### Environment Variables

Set `DEBUG=False` in production and configure:

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=use-a-long-random-secret-key
```

### Collect Static Files

```bash
python manage.py collectstatic
```

### Use Production Server

Install gunicorn:

```bash
pip install gunicorn
```

Run with:

```bash
gunicorn if_phones_were_people.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Background Tasks

Use supervisor or systemd to manage Celery worker and beat processes.

### Database Backups

Set up regular PostgreSQL backups:

```bash
pg_dump -U your_db_user if_phones_were_people_db > backup.sql
```

## Monitoring

### Check Celery Status

```bash
celery -A if_phones_were_people inspect active
celery -A if_phones_were_people inspect stats
```

### View Logs

Check `logs/django.log` for application logs.

### Monitor Redis

```bash
redis-cli ping
redis-cli info
```

## Troubleshooting

### Migration Issues

Reset migrations (development only):

```bash
python manage.py migrate --fake-initial
```

### Celery Not Running Tasks

1. Ensure Redis is running: `redis-cli ping`
2. Check Celery worker logs
3. Verify Celery beat is running for scheduled tasks

### OpenAI API Errors

1. Check API key is set correctly in `.env`
2. Verify you have credits in OpenAI account
3. Check rate limits

### Database Connection Issues

1. Verify PostgreSQL is running
2. Check credentials in `.env`
3. Ensure database exists: `psql -U postgres -l`

## Development Tips

### Django Shell

```bash
python manage.py shell
```

### Create Test Data Quickly

```bash
python manage.py shell < scripts/create_test_data.py
```

### Run Specific Celery Task

```python
from apps.ai_engine.tasks import generate_daily_conversations
result = generate_daily_conversations.delay()
```

### Check API with curl

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Get user data (use token from login response)
curl -X GET http://localhost:8000/api/accounts/users/me/ \
  -H "Authorization: Token your-token-here"
```

## Next Steps

1. Run migrations to set up database
2. Create superuser for admin access
3. Load initial data (device types, categories, traits)
4. Create test user and generate sample data
5. Start all services (Django, Celery worker, Celery beat)
6. Test API endpoints
7. Generate test conversations
8. Customize admin interface
9. Add frontend application

## Support

For issues, check:
- Django logs: `logs/django.log`
- Celery worker output
- Redis connection: `redis-cli ping`
- Database connection: `psql -U your_db_user -d if_phones_were_people_db`
