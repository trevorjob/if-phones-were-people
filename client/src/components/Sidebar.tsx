import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

export default function Sidebar() {
  const location = useLocation();
  
  const isActive = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path);
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>📱💬</h2>
        <span className="app-title">If Phones Were People</span>
      </div>

      <nav className="sidebar-nav">
        <Link 
          to="/" 
          className={`nav-item ${isActive('/') && !location.pathname.includes('/') ? 'active' : ''}`}
        >
          <span className="nav-icon">🏠</span>
          <span className="nav-label">Dashboard</span>
        </Link>

        <Link 
          to="/conversations" 
          className={`nav-item ${isActive('/conversations') ? 'active' : ''}`}
        >
          <span className="nav-icon">💬</span>
          <span className="nav-label">Conversations</span>
        </Link>

        <Link 
          to="/journals" 
          className={`nav-item ${isActive('/journals') ? 'active' : ''}`}
        >
          <span className="nav-icon">📔</span>
          <span className="nav-label">Journals</span>
        </Link>

        <Link 
          to="/analytics" 
          className={`nav-item ${isActive('/analytics') ? 'active' : ''}`}
        >
          <span className="nav-icon">📊</span>
          <span className="nav-label">Analytics</span>
        </Link>

        <Link 
          to="/goals" 
          className={`nav-item ${isActive('/goals') ? 'active' : ''}`}
        >
          <span className="nav-icon">🎯</span>
          <span className="nav-label">Goals</span>
        </Link>

        <Link 
          to="/patterns" 
          className={`nav-item ${isActive('/patterns') ? 'active' : ''}`}
        >
          <span className="nav-icon">🔍</span>
          <span className="nav-label">Patterns</span>
        </Link>

        <Link 
          to="/social" 
          className={`nav-item ${isActive('/social') ? 'active' : ''}`}
        >
          <span className="nav-icon">👥</span>
          <span className="nav-label">Social</span>
        </Link>
      </nav>

      <div className="sidebar-footer">
        <Link to="/settings" className="nav-item">
          <span className="nav-icon">⚙️</span>
          <span className="nav-label">Settings</span>
        </Link>
      </div>
    </aside>
  );
}
