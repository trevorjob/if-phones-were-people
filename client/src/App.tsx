import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import UsageEntry from './components/UsageEntry';
import ConversationsFeed from './pages/ConversationsFeed';
import ConversationDetail from './pages/ConversationDetail';
import Journals from './pages/Journals';
import Analytics from './pages/Analytics';
import Goals from './pages/Goals';
import Patterns from './pages/Patterns';
import Settings from './pages/Settings';
import Sidebar from './components/Sidebar';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user has token
    const token = localStorage.getItem('access_token');
    setIsAuthenticated(!!token);
    setLoading(false);
  }, []);

  const handleAuthSuccess = () => {
    setIsAuthenticated(true);
  };

  if (loading) {
    return (
      <div className="app-loading">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return showRegister ? (
      <Register
        onSuccess={handleAuthSuccess}
        onSwitchToLogin={() => setShowRegister(false)}
      />
    ) : (
      <Login
        onSuccess={handleAuthSuccess}
        onSwitchToRegister={() => setShowRegister(true)}
      />
    );
  }

  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/conversations" element={<ConversationsFeed />} />
            <Route path="/conversations/:id" element={<ConversationDetail />} />
            <Route path="/journals" element={<Journals />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/goals" element={<Goals />} />
            <Route path="/patterns" element={<Patterns />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/device/:deviceId/usage" element={<UsageEntry />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
