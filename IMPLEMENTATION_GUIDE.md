# Implementation Guide - Getting Started

This guide will help you implement the first features and get the app functional.

## Immediate Actions Required

### 1. Fix Critical Bug in Settings

**File:** `server/if_phones_were_people/settings.py`  
**Line:** 55  
**Issue:** Typo - `'apps.applicationss'` has an extra 's'

```python
# WRONG (current)
LOCAL_APPS = [
    'apps.accounts',
    'apps.devices',
    'apps.applicationss',  # ❌ Extra 's'
    ...
]

# CORRECT (should be)
LOCAL_APPS = [
    'apps.accounts',
    'apps.devices',
    'apps.applications',  # ✅ Fixed
    ...
]
```

### 2. Create Environment File

Create `server/.env` with:

```env
# Security
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=if_phones_were_people
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# AI APIs (get these from OpenAI/Anthropic)
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=your-key-here

# App Settings
CONVERSATION_GENERATION_SCHEDULE=0 6 * * *
MAX_DEVICES_PER_USER=10
MAX_FRIEND_CONNECTIONS=50
TEMPORARY_CONNECTION_DEFAULT_HOURS=24
```

### 3. Set Up Database

```bash
# Install PostgreSQL if not installed
# Windows: Download from postgresql.org
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql

# Create database
psql -U postgres
CREATE DATABASE if_phones_were_people;
\q

# Run migrations
cd server
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## Phase 1: Build the REST API (Priority 1)

### Step 1: Create Serializers

Create `server/apps/accounts/serializers.py`:

```python
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'favorite_device_type', 'digital_wellness_goal',
            'friend_code', 'allow_device_invites',
            'daily_summary_enabled', 'conversation_notifications',
            'weekly_insights', 'friend_activity_notifications'
        ]
        read_only_fields = ['friend_code']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'display_name',
            'timezone', 'allow_friend_requests', 'share_usage_stats',
            'public_profile', 'conversation_frequency', 'profile',
            'created_at'
        ]
        read_only_fields = ['id', 'api_key', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        UserProfile.objects.create(user=user)
        return user

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'display_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        UserProfile.objects.create(user=user)
        return user
```

### Step 2: Create API Views

Create `server/apps/accounts/views.py`:

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserRegistrationSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """Get or update current user"""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['get', 'patch'])
    def profile(self, request):
        """Get or update user profile"""
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
```

### Step 3: Create URL Configuration

Create `server/apps/accounts/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

### Step 4: Update Main URLs

Edit `server/if_phones_were_people/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', obtain_auth_token, name='api-token-auth'),
    path('api/accounts/', include('apps.accounts.urls')),
    # Add more apps as you build them
]
```

### Step 5: Test Your API

```bash
# Start server
python manage.py runserver

# Test registration (using curl or Postman)
curl -X POST http://localhost:8000/api/accounts/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "display_name": "Test User"
  }'

# Test login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Use the token from login response
# Test get current user
curl -X GET http://localhost:8000/api/accounts/users/me/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## Phase 2: Device Management API

### Step 1: Device Serializers

Create `server/apps/devices/serializers.py`:

```python
from rest_framework import serializers
from .models import Device, DeviceType, PersonalityTrait, DeviceRelationship

class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = '__all__'

class PersonalityTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalityTrait
        fields = ['id', 'name', 'description', 'category']

class DeviceSerializer(serializers.ModelSerializer):
    personality_traits = PersonalityTraitSerializer(many=True, read_only=True)
    device_type_details = DeviceTypeSerializer(source='device_type', read_only=True)
    
    class Meta:
        model = Device
        fields = [
            'id', 'name', 'device_type', 'device_type_details',
            'platform', 'model_name', 'os_version',
            'personality_type', 'personality_traits',
            'custom_personality_notes', 'is_active', 'is_primary',
            'last_sync', 'last_usage', 'battery_level',
            'created_at', 'personality_description'
        ]
        read_only_fields = ['id', 'created_at', 'personality_description']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class DeviceRelationshipSerializer(serializers.ModelSerializer):
    device_a_details = DeviceSerializer(source='device_a', read_only=True)
    device_b_details = DeviceSerializer(source='device_b', read_only=True)
    
    class Meta:
        model = DeviceRelationship
        fields = '__all__'
```

### Step 2: Device Views

Create `server/apps/devices/views.py`:

```python
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Device, DeviceType, PersonalityTrait, DeviceRelationship
from .serializers import (
    DeviceSerializer, DeviceTypeSerializer,
    PersonalityTraitSerializer, DeviceRelationshipSerializer
)

class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['platform', 'personality_type', 'is_active', 'is_primary']
    search_fields = ['name', 'model_name']
    ordering_fields = ['created_at', 'last_usage', 'name']
    
    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def set_primary(self, request, pk=None):
        """Set this device as primary"""
        device = self.get_object()
        Device.objects.filter(user=request.user, is_primary=True).update(is_primary=False)
        device.is_primary = True
        device.save()
        return Response({'status': 'device set as primary'})
    
    @action(detail=True, methods=['post'])
    def sync(self, request, pk=None):
        """Update last sync time"""
        device = self.get_object()
        from django.utils import timezone
        device.last_sync = timezone.now()
        device.battery_level = request.data.get('battery_level')
        device.save()
        return Response({'status': 'sync successful'})

class DeviceTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer

class PersonalityTraitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PersonalityTrait.objects.all()
    serializer_class = PersonalityTraitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
```

### Step 3: Device URLs

Create `server/apps/devices/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('devices', views.DeviceViewSet, basename='device')
router.register('device-types', views.DeviceTypeViewSet)
router.register('personality-traits', views.PersonalityTraitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

Update main `urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', obtain_auth_token, name='api-token-auth'),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/devices/', include('apps.devices.urls')),  # Add this
]
```

---

## Phase 3: Usage Data Ingestion

Create `server/apps/usage/serializers.py`:

```python
from rest_framework import serializers
from .models import UsageData, AppUsage

class UsageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageData
        fields = '__all__'
        read_only_fields = ['id', 'synced_at', 'updated_at']
    
    def create(self, validated_data):
        # Get or update existing usage data for this device and date
        device = validated_data['device']
        date = validated_data['date']
        
        usage_data, created = UsageData.objects.update_or_create(
            device=device,
            date=date,
            defaults=validated_data
        )
        return usage_data

class AppUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUsage
        fields = '__all__'
        read_only_fields = ['id', 'synced_at', 'updated_at']
```

Create `server/apps/usage/views.py`:

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UsageData, AppUsage
from .serializers import UsageDataSerializer, AppUsageSerializer

class UsageDataViewSet(viewsets.ModelViewSet):
    serializer_class = UsageDataSerializer
    
    def get_queryset(self):
        return UsageData.objects.filter(device__user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        """Upload multiple days of usage data"""
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AppUsageViewSet(viewsets.ModelViewSet):
    serializer_class = AppUsageSerializer
    
    def get_queryset(self):
        return AppUsage.objects.filter(device_app__device__user=self.request.user)
```

---

## Phase 4: AI Integration (Simplified Start)

Create `server/apps/ai_engine/services.py`:

```python
import openai
from django.conf import settings
from typing import List, Dict

openai.api_key = settings.OPENAI_API_KEY

def generate_conversation(
    devices: List,
    apps: List,
    usage_data: Dict,
    conversation_type: str = 'daily_recap'
) -> str:
    """
    Generate a conversation between devices and apps based on usage data
    """
    
    # Build context
    participants = []
    for device in devices:
        participants.append({
            'type': 'device',
            'name': device.name,
            'personality': device.personality_type,
            'description': device.personality_description
        })
    
    for app in apps:
        participants.append({
            'type': 'app',
            'name': app.display_name,
            'personality': app.effective_personality
        })
    
    # Build prompt
    system_prompt = f"""You are creating a humorous conversation between personified devices and apps.
    
Conversation Type: {conversation_type}

Participants:
{format_participants(participants)}

Rules:
1. Each character speaks in line with their personality
2. Make it entertaining and insightful about digital habits
3. Reference actual usage data naturally
4. Keep it under 500 words
5. Format as a script with character names

Usage Context:
{format_usage_data(usage_data)}
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Generate the conversation."}
        ],
        temperature=0.8,
        max_tokens=800
    )
    
    return response.choices[0].message.content

def format_participants(participants: List[Dict]) -> str:
    output = []
    for p in participants:
        output.append(f"- {p['name']} ({p['type']}): {p.get('description', p['personality'])}")
    return '\n'.join(output)

def format_usage_data(usage_data: Dict) -> str:
    return f"""
Screen Time: {usage_data.get('total_screen_time', 0)} minutes
Most Used Apps: {', '.join(usage_data.get('top_apps', []))}
Notable Patterns: {', '.join(usage_data.get('patterns', []))}
"""
```

---

## Quick Commands Cheat Sheet

```bash
# Start development server
python manage.py runserver

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin
python manage.py createsuperuser

# Django shell (for testing)
python manage.py shell

# Start Celery (for background tasks - later)
celery -A if_phones_were_people worker --loglevel=info

# Start Celery Beat (for scheduled tasks - later)
celery -A if_phones_were_people beat --loglevel=info
```

---

## Testing Your Work

### 1. Test User Registration
```python
# In Django shell
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.create_user(
    username='testuser',
    email='test@test.com',
    password='testpass123'
)
print(f"User created: {user.id}")
```

### 2. Test Device Creation
```python
from apps.devices.models import Device, DeviceType

# Create device type
dt = DeviceType.objects.create(
    name='iPhone',
    default_personality='snarky',
    platform_category='mobile'
)

# Create device
device = Device.objects.create(
    user=user,
    name='My iPhone',
    device_type=dt,
    platform='ios',
    personality_type='snarky'
)
print(f"Device created: {device.id}")
```

### 3. Test Usage Data
```python
from apps.usage.models import UsageData
from datetime import date

usage = UsageData.objects.create(
    device=device,
    date=date.today(),
    total_screen_time=240,  # 4 hours
    unlock_count=50,
    collection_method='manual_entry',
    weekday=date.today().weekday(),
    is_weekend=date.today().weekday() >= 5
)
print(f"Usage data created: {usage.id}")
```

---

## Common Issues & Solutions

### Issue: Migration errors
**Solution:** Delete all migration files (except `__init__.py`) and run `makemigrations` again

### Issue: Can't connect to PostgreSQL
**Solution:** Check PostgreSQL is running and credentials in `.env` are correct

### Issue: Import errors
**Solution:** Make sure you're in the `server` directory and virtual environment is activated

### Issue: API returns 401 Unauthorized
**Solution:** Include `Authorization: Token YOUR_TOKEN` header in requests

---

## Next Steps After This

1. Complete serializers for all apps
2. Build conversation generation logic
3. Create admin interface customizations
4. Set up Celery for background tasks
5. Build frontend to consume the API

You now have the foundation! The API is functional and you can start building the AI features and frontend.
