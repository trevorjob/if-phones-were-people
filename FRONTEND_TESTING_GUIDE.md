# Frontend Testing Guide
**Quick reference for testing all MVP features**

---

## 🚀 Quick Start

### 1. Start Backend
```powershell
cd server
python manage.py runserver
```

### 2. Start Frontend
```powershell
cd client
npm run dev
```

### 3. Open Browser
Navigate to: `http://localhost:5173`

---

## ✅ Testing Checklist

### Authentication
- [ ] Register new account
- [ ] Login with credentials
- [ ] Logout
- [ ] Token persistence (refresh page while logged in)

### Dashboard
- [ ] View devices grid
- [ ] Add new device
- [ ] View quick stats (if data exists)
- [ ] View recent conversations (if generated)
- [ ] View recent journals (if generated)
- [ ] Click through to conversations
- [ ] Click through to journals

### Conversations
- [ ] Navigate to Conversations page
- [ ] View conversation cards
- [ ] Click "Generate New" button
- [ ] Filter by type dropdown
- [ ] Filter by mood dropdown
- [ ] Toggle favorites filter
- [ ] Click conversation to view detail
- [ ] Rate conversation (1-5 stars)
- [ ] Toggle favorite status
- [ ] Submit feedback (optional)

### Journals
- [ ] Navigate to Journals page
- [ ] Click "Device Journals" tab
- [ ] Click "App Journals" tab
- [ ] Click "Generate New" button
- [ ] Select journal from list
- [ ] View journal content in detail panel
- [ ] See mood emoji
- [ ] See notable events
- [ ] See mentioned apps/devices

### Analytics
- [ ] Navigate to Analytics page
- [ ] View wellness score circle
- [ ] View 6 quick stat cards
- [ ] View trends section
- [ ] View pattern cards
- [ ] Switch period (weekly/monthly)

### Goals
- [ ] Navigate to Goals page
- [ ] Click "Create Goal" button
- [ ] Select goal type
- [ ] Fill in target values
- [ ] Submit goal creation
- [ ] View goal card
- [ ] Check progress bar
- [ ] Check streak counts
- [ ] Pause/resume goal
- [ ] Delete goal
- [ ] Filter goals (all/active/completed)

### Patterns
- [ ] Navigate to Patterns page
- [ ] View pattern cards
- [ ] Check confidence scores
- [ ] Check strength indicators
- [ ] Check impact indicators
- [ ] Click pattern to view detail
- [ ] View pattern metrics in modal
- [ ] View apps involved
- [ ] Filter patterns (all/active/acknowledged)

### Settings
- [ ] Navigate to Settings page
- [ ] Update first name
- [ ] Update last name
- [ ] Update email
- [ ] Save profile changes
- [ ] Check success message
- [ ] Change password (with current password)
- [ ] Verify password validation (min 8 chars)
- [ ] Verify password match check
- [ ] Logout from settings

### Navigation
- [ ] Click all sidebar links
- [ ] Verify active state highlighting
- [ ] Test back button navigation
- [ ] Test direct URL access
- [ ] Verify logout redirect

---

## 🔍 Manual Generation Testing

### Generate Conversations
1. Navigate to Conversations page
2. Click "Generate New Conversation" button
3. Wait for generation (may take 5-30 seconds)
4. Verify new conversation appears
5. Click to view detail
6. Rate the conversation

### Generate Journals
1. Navigate to Journals page
2. Click "Generate New Journal" button
3. Wait for generation
4. Verify new journals appear in both tabs
5. Select and view journal content

**Note:** Requires OpenAI API key in `.env` file:
```
OPENAI_API_KEY=your_key_here
```

---

## 🐛 Common Issues & Fixes

### Issue: "Generate New" buttons don't work
**Solution:** Check backend console for errors. Ensure OpenAI API key is configured.

### Issue: No data showing in Analytics
**Solution:** Need to add usage data first. Go to a device and enter app usage.

### Issue: 401 Unauthorized errors
**Solution:** Token expired. Logout and login again.

### Issue: Conversations/Journals empty
**Solution:** Click "Generate New" button or wait for scheduled tasks to run.

### Issue: Goals not saving
**Solution:** Check browser console for validation errors. Ensure required fields are filled.

---

## 📊 Test Data Setup

### 1. Add Devices
- Go to Dashboard
- Click "Add Device"
- Add at least 2-3 devices with different personalities

### 2. Enter Usage Data
- Click device card
- Click "📊 Usage"
- Add apps and usage times
- Repeat for multiple days

### 3. Generate AI Content
- Click "Generate New" on Conversations page
- Click "Generate New" on Journals page
- Wait for content to generate

### 4. Create Goals
- Go to Goals page
- Create 2-3 different goal types
- Check progress tracking

---

## 🎯 Expected Behavior

### Conversations
- Should show AI-generated dialogues
- Mood emojis should display
- Rating should save immediately
- Favorites toggle should work
- Filters should update grid

### Journals
- Should show first-person narratives
- Device tabs should switch views
- Notable events should be highlighted
- Apps/devices mentioned should be tagged

### Analytics
- Wellness score should be 0-100
- Stats should reflect actual usage data
- Trends should show top apps/patterns
- Period selector should update data

### Goals
- Progress bar should reflect completion %
- Streaks should increment daily
- Pause should gray out the goal
- Delete should remove permanently

### Patterns
- Should show AI-detected patterns
- Confidence should be percentage
- Impact should be -5 to +5 scale
- Detail modal should show full info

---

## 🚨 Critical Tests

### 1. Auth Flow
Must be able to login → view dashboard → logout → can't access dashboard

### 2. CRUD Operations
- Create device ✓
- Read devices ✓
- Update device (through usage) ✓
- Delete device ✓

### 3. AI Generation
- Generate conversation ✓
- Generate journal ✓
- View generated content ✓

### 4. Data Persistence
- Refresh page → data still there ✓
- Logout/login → data still there ✓

---

## 📱 Mobile Testing

### Responsive Breakpoints
- Desktop: 1200px+
- Tablet: 768px - 1199px
- Mobile: < 768px

### Check on Mobile
- [ ] Sidebar responsive behavior
- [ ] Grid layouts stack vertically
- [ ] Buttons are tappable
- [ ] Forms are usable
- [ ] Modals fit screen
- [ ] Text is readable

---

## 💡 Tips

1. **Use Browser DevTools** - Check Network tab for API errors
2. **Check Console** - Look for JavaScript errors
3. **Test in Incognito** - Verify fresh user experience
4. **Use Multiple Browsers** - Chrome, Firefox, Safari
5. **Clear Local Storage** - For auth testing

---

## 📝 Bug Report Template

```
**Page:** [e.g., Conversations]
**Action:** [e.g., Clicked "Generate New"]
**Expected:** [e.g., New conversation should appear]
**Actual:** [e.g., Got error "API key not configured"]
**Console Error:** [paste error from console]
**Steps to Reproduce:**
1. ...
2. ...
3. ...
```

---

## ✅ MVP Acceptance Criteria

The MVP is ready when:
- ✅ User can register and login
- ✅ User can add devices
- ✅ User can enter usage data
- ✅ User can generate and view conversations
- ✅ User can generate and view journals
- ✅ User can view analytics and stats
- ✅ User can create and track goals
- ✅ User can view detected patterns
- ✅ UI is polished and consistent
- ✅ No console errors during normal use
- ✅ Mobile experience is usable

---

Happy Testing! 🎉
