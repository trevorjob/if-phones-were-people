import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { devicesAPI, appsAPI, deviceAppsAPI, appUsageAPI, usageAPI } from '../services/api';
import './UsageEntry.css';

export default function UsageEntry() {
  const { deviceId } = useParams();
  const navigate = useNavigate();
  
  const [device, setDevice] = useState<any>(null);
  const [deviceApps, setDeviceApps] = useState<any[]>([]);
  const [availableApps, setAvailableApps] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [showAddApp, setShowAddApp] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  
  // Device-level usage data (for journal generation)
  const [deviceUsage, setDeviceUsage] = useState({
    date: new Date(Date.now() - 86400000).toISOString().split('T')[0], // Yesterday
    total_screen_time: 0,
    unlock_count: 0,
    pickup_count: 0,
    notification_count: 0,
    first_pickup_time: '',
    last_usage_time: '',
    battery_start_percent: 100,
    battery_end_percent: 100,
    collection_method: "manual_entry",
    weekday: 4
  });
  
  // App-level usage entries
  const [usageEntries, setUsageEntries] = useState<any[]>([{
    id: Date.now(),
    device_app: '',
    date: new Date(Date.now() - 86400000).toISOString().split('T')[0], // Yesterday
    time_spent_minutes: 0,
    launch_count: 1,
  }]);

  useEffect(() => {
    loadData();
  }, [deviceId]);

  const loadData = async () => {
    try {
      const [deviceRes, appsRes, allAppsRes] = await Promise.all([
        devicesAPI.get(deviceId!),
        deviceAppsAPI.list(deviceId),
        appsAPI.list(),
      ]);

      setDevice(deviceRes.data);
      setDeviceApps(appsRes.data.results || appsRes.data);
      setAvailableApps(allAppsRes.data.results || allAppsRes.data);
    } catch (error) {
      console.error('Failed to load data:', error);
      alert('Failed to load device data');
    } finally {
      setLoading(false);
    }
  };  const addUsageEntry = () => {
    setUsageEntries([...usageEntries, {
      id: Date.now(),
      device_app: '',
      date: deviceUsage.date, // Use same date as device usage
      time_spent_minutes: 0,
      launch_count: 1,
    }]);
  };

  const removeUsageEntry = (id: number) => {
    setUsageEntries(usageEntries.filter(entry => entry.id !== id));
  };

  const updateUsageEntry = (id: number, field: string, value: any) => {
    setUsageEntries(usageEntries.map(entry => 
      entry.id === id ? { ...entry, [field]: value } : entry
    ));
  };

  const handleInstallApp = async (appId: number) => {
    try {
      await deviceAppsAPI.create({
        device: deviceId,
        app: appId,
      });
      await loadData();
      setShowAddApp(false);
      setSearchQuery('');
    } catch (error) {
      console.error('Failed to install app:', error);
      alert('Failed to install app');
    }
  };  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate device usage
    if (deviceUsage.total_screen_time <= 0) {
      alert('Please enter total screen time for the device');
      return;
    }
    
    // Validate app entries
    const invalidEntries = usageEntries.filter(e => !e.device_app || e.time_spent_minutes <= 0);
    if (invalidEntries.length > 0) {
      alert('Please fill in all app usage fields with valid data');
      return;
    }

    setSubmitting(true);
    try {
      // 1. Submit device-level usage data first
      const deviceUsageData = {
        device: deviceId,
        date: deviceUsage.date,
        total_screen_time: deviceUsage.total_screen_time,
        unlock_count: deviceUsage.unlock_count,
        pickup_count: deviceUsage.pickup_count,
        notification_count: deviceUsage.notification_count,
        first_pickup_time: deviceUsage.first_pickup_time || null,
        last_usage_time: deviceUsage.last_usage_time || null,
        battery_start_percent: deviceUsage.battery_start_percent,
        battery_end_percent: deviceUsage.battery_end_percent,
        collection_method: "manual_entry",
        weekday: 4
      };
      
      await usageAPI.create(deviceUsageData);
      
      // 2. Submit app-level usage data
      const appUsageData = usageEntries.map(entry => ({
        device_app: entry.device_app,
        date: entry.date,
        time_spent_minutes: entry.time_spent_minutes,
        launch_count: entry.launch_count,
      }));

      await appUsageAPI.bulkCreate(appUsageData);
      
      alert('Usage data submitted successfully! You can now generate journals for this device.');
      navigate('/');
    } catch (error: any) {
      console.error('Failed to submit usage data:', error);
      alert(error.response?.data?.detail || 'Failed to submit usage data');
    } finally {
      setSubmitting(false);
    }
  };

  const filteredApps = availableApps.filter(app =>
    app.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const installedAppIds = deviceApps.map(da => da.app.id);
  const uninstalledApps = filteredApps.filter(app => !installedAppIds.includes(app.id));

  if (loading) {
    return (
      <div className="usage-loading">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="usage-entry-page">
      <header className="page-header">
        <div className="header-content">
          <button onClick={() => navigate('/')} className="back-button">
            ← Back
          </button>
          <div>
            <h1>Manual Usage Entry</h1>
            <p className="device-name">{device?.name}</p>
          </div>
        </div>
      </header>

      <main className="usage-main">
        <div className="usage-container">
          {deviceApps.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📱</div>
              <h3>No apps installed</h3>
              <p>Install some apps on this device first to track usage</p>
              <button onClick={() => setShowAddApp(true)} className="btn-primary">
                Install Apps
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit}>
              <div className="form-header">
                <h2>Usage Entries</h2>
                <div className="header-actions">
                  <button
                    type="button"
                    onClick={() => setShowAddApp(true)}
                    className="btn-secondary"
                  >
                    + Install App
                  </button>
                  <button
                    type="button"
                    onClick={addUsageEntry}
                    className="btn-secondary"
                  >
                    + Add Entry
                  </button>
                </div>
              </div>

              {/* Device-Level Usage Stats */}
              <div className="device-stats-section">
                <h3>📱 Device Stats for {deviceUsage.date}</h3>
                <p className="section-description">
                  Enter overall device usage statistics for yesterday. These are required for journal generation.
                </p>
                
                <div className="device-stats-grid">
                  <div className="form-group">
                    <label>Date *</label>
                    <input
                      type="date"
                      value={deviceUsage.date}
                      onChange={(e) => {
                        const newDate = e.target.value;
                        setDeviceUsage({ ...deviceUsage, date: newDate });
                        // Update all app entries to match
                        setUsageEntries(usageEntries.map(entry => ({ ...entry, date: newDate })));
                      }}
                      required
                      max={new Date(Date.now() - 86400000).toISOString().split('T')[0]}
                    />
                  </div>

                  <div className="form-group">
                    <label>Total Screen Time (minutes) *</label>
                    <input
                      type="number"
                      value={deviceUsage.total_screen_time}
                      onChange={(e) => setDeviceUsage({ ...deviceUsage, total_screen_time: parseInt(e.target.value) || 0 })}
                      required
                      min="0"
                      placeholder="e.g., 240"
                    />
                    <small>{deviceUsage.total_screen_time > 0 && `≈ ${Math.floor(deviceUsage.total_screen_time / 60)}h ${deviceUsage.total_screen_time % 60}m`}</small>
                  </div>

                  <div className="form-group">
                    <label>Unlock Count *</label>
                    <input
                      type="number"
                      value={deviceUsage.unlock_count}
                      onChange={(e) => setDeviceUsage({ ...deviceUsage, unlock_count: parseInt(e.target.value) || 0 })}
                      required
                      min="0"
                      placeholder="e.g., 80"
                    />
                  </div>

                  <div className="form-group">
                    <label>Pickup Count *</label>
                    <input
                      type="number"
                      value={deviceUsage.pickup_count}
                      onChange={(e) => setDeviceUsage({ ...deviceUsage, pickup_count: parseInt(e.target.value) || 0 })}
                      required
                      min="0"
                      placeholder="e.g., 50"
                    />
                  </div>

                  <div className="form-group">
                    <label>Notification Count</label>
                    <input
                      type="number"
                      value={deviceUsage.notification_count}
                      onChange={(e) => setDeviceUsage({ ...deviceUsage, notification_count: parseInt(e.target.value) || 0 })}
                      min="0"
                      placeholder="e.g., 120"
                    />
                  </div>

                  <div className="form-group">
                    <label>First Pickup Time</label>
                    <input
                      type="time"
                      value={deviceUsage.first_pickup_time}
                      onChange={(e) => setDeviceUsage({ ...deviceUsage, first_pickup_time: e.target.value })}
                    />
                  </div>

                  <div className="form-group">
                    <label>Last Usage Time</label>
                    <input
                      type="time"
                      value={deviceUsage.last_usage_time}
                      onChange={(e) => setDeviceUsage({ ...deviceUsage, last_usage_time: e.target.value })}
                    />
                  </div>

                  <div className="form-group">
                    <label>Battery Start %</label>
                    <input
                      type="number"
                      value={deviceUsage.battery_start_percent}
                      onChange={(e) => setDeviceUsage({ ...deviceUsage, battery_start_percent: parseInt(e.target.value) || 100 })}
                      min="0"
                      max="100"
                      placeholder="100"
                    />
                  </div>

                  <div className="form-group">
                    <label>Battery End %</label>
                    <input
                      type="number"
                      value={deviceUsage.battery_end_percent}
                      onChange={(e) => setDeviceUsage({ ...deviceUsage, battery_end_percent: parseInt(e.target.value) || 100 })}
                      min="0"
                      max="100"
                      placeholder="20"
                    />
                  </div>
                </div>
              </div>

              {/* App-Level Usage Entries */}
              <h3 style={{ marginTop: '2rem' }}>📲 App Usage</h3>
              <div className="usage-entries">
                {usageEntries.map((entry, index) => (
                  <div key={entry.id} className="usage-entry-card">
                    <div className="entry-header">
                      <span className="entry-number">Entry #{index + 1}</span>
                      {usageEntries.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeUsageEntry(entry.id)}
                          className="remove-button"
                        >
                          Remove
                        </button>
                      )}
                    </div>

                    <div className="entry-fields">
                      <div className="form-group">
                        <label>App *</label>
                        <select
                          value={entry.device_app}
                          onChange={(e) => updateUsageEntry(entry.id, 'device_app', e.target.value)}
                          required
                        >
                          <option value="">Select app...</option>
                          {deviceApps.map((deviceApp) => (
                            <option key={deviceApp.id} value={deviceApp.id}>
                              {deviceApp.app_name || deviceApp.app.name}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div className="form-group">
                        <label>Date *</label>
                        <input
                          type="date"
                          value={entry.date}
                          onChange={(e) => updateUsageEntry(entry.id, 'date', e.target.value)}
                          required
                          max={new Date().toISOString().split('T')[0]}
                        />
                      </div>                      <div className="form-group">
                        <label>Duration (minutes) *</label>
                        <input
                          type="number"
                          value={entry.time_spent_minutes}
                          onChange={(e) => updateUsageEntry(entry.id, 'time_spent_minutes', parseInt(e.target.value))}
                          required
                          min="1"
                          placeholder="e.g., 45"
                        />
                      </div>

                      <div className="form-group">
                        <label>Times Opened</label>
                        <input
                          type="number"
                          value={entry.launch_count}
                          onChange={(e) => updateUsageEntry(entry.id, 'launch_count', parseInt(e.target.value))}
                          min="1"
                          placeholder="e.g., 5"
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="form-actions">
                <button type="button" onClick={() => navigate('/')} className="btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn-primary" disabled={submitting}>
                  {submitting ? 'Submitting...' : `Submit ${usageEntries.length} ${usageEntries.length === 1 ? 'Entry' : 'Entries'}`}
                </button>
              </div>
            </form>
          )}
        </div>
      </main>

      {showAddApp && (
        <div className="modal-overlay" onClick={() => setShowAddApp(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Install Apps</h2>
              <button className="close-button" onClick={() => setShowAddApp(false)}>×</button>
            </div>

            <div className="modal-body">
              <input
                type="text"
                className="search-input"
                placeholder="Search apps..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                autoFocus
              />

              <div className="apps-list">
                {uninstalledApps.length === 0 ? (
                  <p className="no-apps">
                    {searchQuery ? 'No apps found' : 'All apps are already installed'}
                  </p>
                ) : (
                  uninstalledApps.map((app) => (
                    <div key={app.id} className="app-item">
                      <div className="app-info">
                        <div className="app-name">{app.name}</div>
                        <div className="app-category">{app.category?.name}</div>
                      </div>
                      <button
                        onClick={() => handleInstallApp(app.id)}
                        className="btn-install"
                      >
                        Install
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
