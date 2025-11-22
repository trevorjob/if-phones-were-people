import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  devicesAPI, 
  deviceTypesAPI, 
  personalityTraitsAPI,
  conversationsAPI,
  journalsAPI,
  analyticsAPI
} from '../services/api';
import DeviceCard from './DeviceCard';
import AddDevice from './AddDevice';
import './Dashboard.css';

interface Device {
  id: string;
  name: string;
  device_type: any;
  platform: string;
  personality_type: string;
  is_active: boolean;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [devices, setDevices] = useState<Device[]>([]);
  const [showAddDevice, setShowAddDevice] = useState(false);
  const [deviceTypes, setDeviceTypes] = useState([]);
  const [personalityTraits, setPersonalityTraits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<any>(null);
  const [recentConversations, setRecentConversations] = useState<any[]>([]);
  const [recentJournals, setRecentJournals] = useState<any[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [devicesRes, typesRes, traitsRes] = await Promise.all([
        devicesAPI.list(),
        deviceTypesAPI.list(),
        personalityTraitsAPI.list(),
      ]);

      setDevices(devicesRes.data.results || devicesRes.data);
      setDeviceTypes(typesRes.data.results || typesRes.data);
      setPersonalityTraits(traitsRes.data.results || traitsRes.data);

      // Load additional dashboard data
      loadDashboardStats();
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadDashboardStats = async () => {
    try {
      const [statsRes, conversationsRes, journalsRes] = await Promise.all([
        analyticsAPI.stats.latest().catch(() => ({ data: null })),
        conversationsAPI.recent().catch(() => ({ data: [] })),
        journalsAPI.deviceJournals.recent().catch(() => ({ data: [] })),
      ]);

      setStats(statsRes.data);
      setRecentConversations(conversationsRes.data.results?.slice(0, 3) || conversationsRes.data?.slice(0, 3) || []);
      setRecentJournals(journalsRes.data.results?.slice(0, 3) || journalsRes.data?.slice(0, 3) || []);
    } catch (error) {
      console.error('Failed to load dashboard stats:', error);
    }
  };

  const handleLogout = () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      // Optional: call logout endpoint
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.reload();
  };

  const handleDeviceAdded = () => {
    setShowAddDevice(false);
    loadData();
  };

  const handleDeviceDeleted = () => {
    loadData();
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading your devices...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>📱 If Phones Were People</h1>
          <button onClick={handleLogout} className="btn-secondary">
            Logout
          </button>
        </div>
      </header>      <main className="dashboard-main">
        <div className="dashboard-content">
          {/* Quick Stats Section */}
          {stats && (
            <div className="quick-stats">
              <div className="stat-card">
                <div className="stat-icon">💯</div>
                <div className="stat-info">
                  <span className="stat-label">Wellness Score</span>
                  <span className="stat-value">{stats.wellness_score || 0}</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">⏱️</div>
                <div className="stat-info">
                  <span className="stat-label">Screen Time Today</span>
                  <span className="stat-value">{Math.round((stats.total_screen_time_minutes || 0) / 60)}h</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">📱</div>
                <div className="stat-info">
                  <span className="stat-label">Pickups</span>
                  <span className="stat-value">{stats.total_pickups || 0}</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">🔔</div>
                <div className="stat-info">
                  <span className="stat-label">Notifications</span>
                  <span className="stat-value">{stats.total_notifications || 0}</span>
                </div>
              </div>
            </div>
          )}

          {/* Recent Activity */}
          {(recentConversations.length > 0 || recentJournals.length > 0) && (
            <div className="recent-activity">
              {recentConversations.length > 0 && (
                <div className="activity-section">
                  <div className="section-header">
                    <h3>Recent Conversations</h3>
                    <button onClick={() => navigate('/conversations')} className="btn-link">
                      View All →
                    </button>
                  </div>
                  <div className="activity-cards">
                    {recentConversations.map((conv: any) => (
                      <div 
                        key={conv.id} 
                        className="activity-card"
                        onClick={() => navigate(`/conversations/${conv.id}`)}
                      >
                        <div className="activity-header">
                          <span className="activity-type">{conv.conversation_type?.replace('_', ' ')}</span>
                          <span className="activity-mood">{conv.mood_emoji}</span>
                        </div>
                        <p className="activity-preview">{conv.content?.substring(0, 100)}...</p>
                        <span className="activity-date">{new Date(conv.date).toLocaleDateString()}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {recentJournals.length > 0 && (
                <div className="activity-section">
                  <div className="section-header">
                    <h3>Recent Journal Entries</h3>
                    <button onClick={() => navigate('/journals')} className="btn-link">
                      View All →
                    </button>
                  </div>
                  <div className="activity-cards">
                    {recentJournals.map((journal: any) => (
                      <div 
                        key={journal.id} 
                        className="activity-card"
                        onClick={() => navigate('/journals')}
                      >
                        <div className="activity-header">
                          <span className="activity-type">📔 {journal.device?.name || 'Device'} Journal</span>
                          <span className="activity-mood">{journal.mood_emoji}</span>
                        </div>
                        <p className="activity-preview">{journal.content?.substring(0, 100)}...</p>
                        <span className="activity-date">{new Date(journal.date).toLocaleDateString()}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          <div className="section-header">
            <h2>My Devices</h2>
            <button 
              onClick={() => setShowAddDevice(true)} 
              className="btn-primary"
            >
              + Add Device
            </button>
          </div>

          {devices.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📱</div>
              <h3>No devices yet</h3>
              <p>Add your first device to get started!</p>
              <button 
                onClick={() => setShowAddDevice(true)} 
                className="btn-primary"
              >
                Add Your First Device
              </button>
            </div>
          ) : (
            <div className="devices-grid">
              {devices.map((device) => (
                <DeviceCard 
                  key={device.id} 
                  device={device} 
                  onDeleted={handleDeviceDeleted}
                />
              ))}
            </div>
          )}
        </div>
      </main>

      {showAddDevice && (
        <AddDevice
          deviceTypes={deviceTypes}
          personalityTraits={personalityTraits}
          onClose={() => setShowAddDevice(false)}
          onAdded={handleDeviceAdded}
        />
      )}
    </div>
  );
}
