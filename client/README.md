# If Phones Were People - Frontend

Simple React frontend for manual data entry and testing the backend API.

## 🚀 Quick Start

```bash
cd client
npm install
npm run dev
```

App runs on **http://localhost:5173**

## ✨ Features

- 🔐 Login/Register with JWT
- 📱 Device Management  
- 📊 Manual Usage Entry
- 🎯 App Installation
- 🎨 Clean, Responsive UI

## 📋 Usage Flow

1. **Register/Login** → Create account
2. **Add Device** → Add your phone/laptop with personality
3. **Install Apps** → Search and install apps
4. **Enter Usage** → Manually log app usage data
5. **Test Backend** → Verify API integration

## ⚠️ Temporary Tool

This is a **temporary manual entry interface** for testing. Production will have automated data collection from devices.

## 🛠️ Tech Stack

- React 18 + TypeScript
- Vite
- React Router
- Axios
- CSS (no framework)

## 📁 Structure

```
src/
├── components/       # UI components
├── services/         # API layer
├── App.tsx          # Main app
└── main.tsx         # Entry point
```

## 🔌 Backend Connection

- Django backend: `http://localhost:8000`
- API proxy configured in `vite.config.ts`
- Ensure backend is running first!

## 🧪 Testing Checklist

- [ ] Start Django backend (`python manage.py runserver`)
- [ ] Run seed data (`python manage.py seed_data`)
- [ ] Start frontend (`npm run dev`)
- [ ] Register new account
- [ ] Add a device
- [ ] Install apps
- [ ] Enter usage data
- [ ] Verify data in Django admin

---

**Made for testing "If Phones Were People" backend** 🎭📱
