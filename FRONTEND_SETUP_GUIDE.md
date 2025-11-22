# Frontend + Backend Setup Guide

Complete guide to run the full stack application with manual data entry.

## 🎯 Overview

This guide will help you set up:
1. Django backend (API server)
2. React frontend (manual data entry UI)
3. Seed data (device types, apps, etc.)

## ⚡ Quick Start (5 minutes)

### Terminal 1 - Backend
```bash
cd server
venv\Scripts\activate
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

### Terminal 2 - Frontend
```bash
cd client
npm install
npm run dev
```

### Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api
- Django Admin: http://localhost:8000/admin

## 📋 Detailed Setup

### Prerequisites

✅ Python 3.10+ installed  
✅ Node.js 18+ installed  
✅ Git installed

### Step 1: Backend Setup

1. **Navigate to server directory:**
   ```bash
   cd server
   ```

2. **Create & activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Load seed data:**
   ```bash
   python manage.py seed_data
   ```
   
   This creates:
   - 5 device types
   - 16 personality traits
   - 10 app categories
   - 13 popular apps
   - 12 conversation triggers

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start backend server:**
   ```bash
   python manage.py runserver
   ```
   
   ✅ Backend running at http://localhost:8000

### Step 2: Frontend Setup

1. **Open new terminal and navigate to client:**
   ```bash
   cd client
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   
   ✅ Frontend running at http://localhost:5173

## 🧪 Testing the Flow

### 1. Register an Account

1. Open http://localhost:5173
2. Click "Register here"
3. Fill in details:
   - First Name: John
   - Last Name: Doe
   - Username: johndoe
   - Email: john@example.com
   - Password: (minimum 8 characters)
4. Click "Create Account"

✅ You're automatically logged in!

### 2. Add Your First Device

1. Click "+ Add Device"
2. Fill in:
   - **Name:** My iPhone
   - **Device Type:** Smartphone
   - **Platform:** iOS
   - **Model Name:** iPhone 15 Pro
   - **Primary Personality:** Social Butterfly
   - **Additional Traits:** Gossipy, Anxious (optional)
3. Click "Add Device"

✅ Device card appears on dashboard!

### 3. Install Apps

1. Click "View Details" on your device
2. Click "+ Install App"
3. Search for apps (e.g., "Instagram")
4. Click "Install" on desired apps
5. Install multiple apps:
   - Instagram
   - TikTok
   - YouTube
   - Gmail
   - Spotify

✅ Apps now installed on device!

### 4. Enter Usage Data

1. From dashboard, click "Add Usage" on device
2. Fill in usage entry:
   - **App:** Instagram
   - **Date:** Today's date
   - **Duration:** 45 (minutes)
   - **Times Opened:** 8
3. Click "+ Add Entry" to add more
4. Add another entry:
   - **App:** TikTok
   - **Date:** Today's date
   - **Duration:** 90 (minutes)
   - **Times Opened:** 15
5. Click "Submit"

✅ Usage data saved to backend!

### 5. Verify in Django Admin

1. Navigate to http://localhost:8000/admin
2. Login with superuser credentials
3. Check:
   - **Devices** → See your device
   - **Device Apps** → See installed apps
   - **Usage Data** → See your usage entries
   - **Apps** → See seed data apps
   - **Device Types** → See seed data

✅ All data is in the database!

## 🔍 Verification Checklist

Run these checks to ensure everything works:

### Backend Health Check
```bash
# In server directory
curl http://localhost:8000/api/
# Should return API root with endpoints
```

### Seed Data Verification
```bash
python manage.py shell -c "
from apps.devices.models import DeviceType, PersonalityTrait
from apps.applications.models import App, AppCategory
print(f'Device Types: {DeviceType.objects.count()}')
print(f'Personality Traits: {PersonalityTrait.objects.count()}')
print(f'App Categories: {AppCategory.objects.count()}')
print(f'Apps: {App.objects.count()}')
"
```

Expected output:
```
Device Types: 5
Personality Traits: 16
App Categories: 10
Apps: 13
```

### Frontend Health Check
- Visit http://localhost:5173
- Should see login page
- No console errors

### API Connection Test
Open browser console on frontend and run:
```javascript
fetch('http://localhost:8000/api/device-types/')
  .then(r => r.json())
  .then(console.log)
```

Should return list of device types.

## 📊 Test Data Scenarios

### Scenario 1: Social Media Heavy User
```
Device: My iPhone (Social personality)
Apps: Instagram, TikTok, Twitter/X, WhatsApp
Usage:
  - TikTok: 120 min, 20 opens
  - Instagram: 90 min, 15 opens
  - Twitter/X: 45 min, 10 opens
  - WhatsApp: 60 min, 30 opens
```

### Scenario 2: Workaholic
```
Device: My Laptop (Workaholic personality)
Apps: Slack, Gmail, Notion, Zoom
Usage:
  - Slack: 180 min, 50 opens
  - Gmail: 120 min, 40 opens
  - Notion: 90 min, 10 opens
```

### Scenario 3: Entertainment Lover
```
Device: My Tablet (Chill personality)
Apps: Netflix, YouTube, Spotify
Usage:
  - Netflix: 240 min, 3 opens
  - YouTube: 180 min, 25 opens
  - Spotify: 300 min, 8 opens
```

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'rest_framework'`
```bash
# Solution:
pip install -r requirements.txt
```

**Problem:** `django.db.utils.OperationalError: no such table`
```bash
# Solution:
python manage.py migrate
```

**Problem:** `Port 8000 already in use`
```bash
# Solution: Run on different port
python manage.py runserver 8001
# Then update frontend API URL
```

### Frontend Issues

**Problem:** `Cannot connect to backend`
- Ensure backend is running on port 8000
- Check CORS settings in Django
- Verify vite.config.ts proxy settings

**Problem:** `401 Unauthorized errors`
- Login again
- Check token in localStorage
- Verify JWT configuration

**Problem:** `Module not found`
```bash
# Solution:
cd client
npm install
```

### Seed Data Issues

**Problem:** Seed data not loading
```bash
# Solution: Run with reset flag
python manage.py seed_data --reset
```

**Problem:** Duplicate entries
```bash
# Solution: Command is idempotent, just run again
python manage.py seed_data
```

## 🔧 Configuration

### Environment Variables

Create `.env` in server directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### API Base URL

Frontend API URL is configured in:
- `client/src/services/api.ts` (hardcoded)
- `client/vite.config.ts` (proxy)

To change:
```typescript
// In api.ts
const API_BASE_URL = 'http://your-backend-url/api';
```

## 📝 Development Workflow

### Daily Development
```bash
# Terminal 1 - Backend
cd server
venv\Scripts\activate
python manage.py runserver

# Terminal 2 - Frontend  
cd client
npm run dev
```

### Making Changes

**Backend Changes:**
- Edit models → Run migrations
- Edit views/serializers → Restart server
- Edit settings → Restart server

**Frontend Changes:**
- Edit components → Auto-reload (HMR)
- Edit API calls → Check network tab
- Install packages → Restart dev server

### Database Reset
```bash
# WARNING: Deletes all data!
cd server
Remove-Item db.sqlite3
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
```

## 🚀 Next Steps

Once everything is working:

1. **Test API Endpoints**
   - Try all CRUD operations
   - Test authentication flow
   - Verify data relationships

2. **Check Conversations** (if AI configured)
   - Ensure OpenAI API key is set
   - Try generating conversations
   - Check conversation triggers

3. **Explore Django Admin**
   - View all models
   - Test inline editing
   - Check relationships

4. **Plan Automated Data Collection**
   - This manual entry is temporary
   - Design mobile data collection
   - Plan data sync strategy

## 📚 Resources

- Backend API: `server/SETUP_GUIDE.md`
- Seed Data: `server/SEED_DATA_DOCUMENTATION.md`
- Frontend: `client/README.md`
- Project Status: `PROJECT_STATUS.md`

## ✅ Success Criteria

You've successfully set up the system when:

- [ ] Backend runs without errors
- [ ] Frontend loads at http://localhost:5173
- [ ] Can register and login
- [ ] Can create devices
- [ ] Can install apps
- [ ] Can submit usage data
- [ ] Data appears in Django admin
- [ ] No CORS errors
- [ ] No console errors

## 🎉 You're Ready!

Your full-stack development environment is ready for testing the backend flow with manual data entry.

**Remember:** This manual entry UI is temporary for testing. Production will have automated data collection from actual devices.

---

**Happy Testing!** 🚀
