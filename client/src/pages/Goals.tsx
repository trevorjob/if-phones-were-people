import { useState, useEffect } from 'react';
import { goalsAPI, devicesAPI, appsAPI } from '../services/api';
import './Goals.css';

interface Goal {
  id: string;
  goal_type: string;
  device?: { id: string; name: string };
  app?: { id: string; display_name: string };
  target_minutes_daily?: number;
  target_sessions_daily?: number;
  cutoff_time?: string;
  start_date: string;
  end_date?: string;
  duration_days?: number;
  current_streak: number;
  best_streak: number;
  total_successful_days: number;
  is_active: boolean;
  completion_percentage: number;
  notes?: string;
}

interface Device {
  id: string;
  name: string;
}

interface App {
  id: string;
  display_name: string;
}

export default function Goals() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [devices, setDevices] = useState<Device[]>([]);
  const [apps, setApps] = useState<App[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('active');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [goalsRes, devicesRes, appsRes] = await Promise.all([
        goalsAPI.list(),
        devicesAPI.list(),
        appsAPI.list(),
      ]);

      setGoals(goalsRes.data.results || goalsRes.data || []);
      setDevices(devicesRes.data.results || devicesRes.data || []);
      setApps(appsRes.data.results || appsRes.data || []);
    } catch (error) {
      console.error('Failed to load goals:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateGoal = async (goalData: any) => {
    try {
      await goalsAPI.create(goalData);
      setShowCreateModal(false);
      loadData();
    } catch (error) {
      console.error('Failed to create goal:', error);
    }
  };

  const handleDeleteGoal = async (goalId: string) => {
    if (!window.confirm('Are you sure you want to delete this goal?')) return;
    
    try {
      await goalsAPI.delete(goalId);
      loadData();
    } catch (error) {
      console.error('Failed to delete goal:', error);
    }
  };

  const handleToggleActive = async (goal: Goal) => {
    try {
      await goalsAPI.update(goal.id, { is_active: !goal.is_active });
      loadData();
    } catch (error) {
      console.error('Failed to update goal:', error);
    }
  };

  const getGoalTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      reduce_total: 'Reduce Total Screen Time',
      reduce_app: 'Reduce App Usage',
      increase_productive: 'Increase Productive Apps',
      limit_daily: 'Daily Time Limit',
      digital_sunset: 'Digital Sunset',
      weekend_detox: 'Weekend Detox',
      focus_sessions: 'Focus Sessions',
      app_replacement: 'Replace App',
    };
    return labels[type] || type;
  };

  const getGoalIcon = (type: string) => {
    const icons: Record<string, string> = {
      reduce_total: '📉',
      reduce_app: '🎯',
      increase_productive: '📈',
      limit_daily: '⏰',
      digital_sunset: '🌅',
      weekend_detox: '🌴',
      focus_sessions: '🎯',
      app_replacement: '🔄',
    };
    return icons[type] || '🎯';
  };

  const getStreakColor = (streak: number) => {
    if (streak >= 7) return 'green';
    if (streak >= 3) return 'orange';
    return 'gray';
  };

  const filteredGoals = goals.filter((goal) => {
    if (filter === 'active') return goal.is_active;
    if (filter === 'completed') return !goal.is_active && goal.completion_percentage >= 100;
    return true;
  });

  if (loading) {
    return (
      <div className="goals-loading">
        <div className="spinner"></div>
        <p>Loading goals...</p>
      </div>
    );
  }

  return (
    <div className="goals-page">
      <header className="goals-header">
        <div className="header-content">
          <h1>🎯 My Goals</h1>
          <button onClick={() => setShowCreateModal(true)} className="btn-primary">
            + Create Goal
          </button>
        </div>
      </header>

      <div className="goals-filters">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Goals
        </button>
        <button
          className={`filter-btn ${filter === 'active' ? 'active' : ''}`}
          onClick={() => setFilter('active')}
        >
          Active
        </button>
        <button
          className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
          onClick={() => setFilter('completed')}
        >
          Completed
        </button>
      </div>

      {filteredGoals.length === 0 ? (
        <div className="goals-empty">
          <div className="empty-icon">🎯</div>
          <h3>No goals yet</h3>
          <p>Set your first digital wellness goal to get started!</p>
          <button onClick={() => setShowCreateModal(true)} className="btn-primary">
            Create Your First Goal
          </button>
        </div>
      ) : (
        <div className="goals-grid">
          {filteredGoals.map((goal) => (
            <div key={goal.id} className={`goal-card ${!goal.is_active ? 'inactive' : ''}`}>
              <div className="goal-header">
                <div className="goal-type">
                  <span className="goal-icon">{getGoalIcon(goal.goal_type)}</span>
                  <span className="goal-type-label">{getGoalTypeLabel(goal.goal_type)}</span>
                </div>
                <button
                  className="goal-menu-btn"
                  onClick={() => handleDeleteGoal(goal.id)}
                  title="Delete goal"
                >
                  🗑️
                </button>
              </div>

              {goal.device && (
                <div className="goal-target">
                  <strong>Device:</strong> {goal.device.name}
                </div>
              )}

              {goal.app && (
                <div className="goal-target">
                  <strong>App:</strong> {goal.app.display_name}
                </div>
              )}

              {goal.target_minutes_daily && (
                <div className="goal-target">
                  <strong>Target:</strong> {goal.target_minutes_daily} minutes/day
                </div>
              )}

              {goal.cutoff_time && (
                <div className="goal-target">
                  <strong>Cutoff Time:</strong> {goal.cutoff_time}
                </div>
              )}

              <div className="goal-progress">
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${Math.min(goal.completion_percentage, 100)}%` }}
                  />
                </div>
                <span className="progress-label">{goal.completion_percentage.toFixed(0)}%</span>
              </div>

              <div className="goal-stats">
                <div className="stat">
                  <span className="stat-label">Current Streak</span>
                  <span className={`stat-value streak-${getStreakColor(goal.current_streak)}`}>
                    🔥 {goal.current_streak} days
                  </span>
                </div>
                <div className="stat">
                  <span className="stat-label">Best Streak</span>
                  <span className="stat-value">⭐ {goal.best_streak} days</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Success Rate</span>
                  <span className="stat-value">
                    ✅ {goal.total_successful_days} days
                  </span>
                </div>
              </div>

              {goal.notes && (
                <div className="goal-notes">
                  <strong>Notes:</strong> {goal.notes}
                </div>
              )}

              <div className="goal-footer">
                <span className="goal-dates">
                  {new Date(goal.start_date).toLocaleDateString()}
                  {goal.end_date && ` - ${new Date(goal.end_date).toLocaleDateString()}`}
                </span>
                <button
                  className={`btn-toggle ${goal.is_active ? 'active' : 'inactive'}`}
                  onClick={() => handleToggleActive(goal)}
                >
                  {goal.is_active ? 'Pause' : 'Resume'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {showCreateModal && (
        <CreateGoalModal
          devices={devices}
          apps={apps}
          onClose={() => setShowCreateModal(false)}
          onCreate={handleCreateGoal}
        />
      )}
    </div>
  );
}

interface CreateGoalModalProps {
  devices: Device[];
  apps: App[];
  onClose: () => void;
  onCreate: (goalData: any) => void;
}

function CreateGoalModal({ devices, apps, onClose, onCreate }: CreateGoalModalProps) {
  const [goalType, setGoalType] = useState('reduce_total');
  const [deviceId, setDeviceId] = useState('');
  const [appId, setAppId] = useState('');
  const [targetMinutes, setTargetMinutes] = useState('');
  const [cutoffTime, setCutoffTime] = useState('');
  const [durationDays, setDurationDays] = useState('30');
  const [notes, setNotes] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const goalData: any = {
      goal_type: goalType,
      duration_days: parseInt(durationDays),
      notes,
    };

    if (deviceId) goalData.device = deviceId;
    if (appId) goalData.app = appId;
    if (targetMinutes) goalData.target_minutes_daily = parseInt(targetMinutes);
    if (cutoffTime) goalData.cutoff_time = cutoffTime;

    onCreate(goalData);
  };

  const goalTypes = [
    { value: 'reduce_total', label: '📉 Reduce Total Screen Time' },
    { value: 'reduce_app', label: '🎯 Reduce Specific App Usage' },
    { value: 'increase_productive', label: '📈 Increase Productive Apps' },
    { value: 'limit_daily', label: '⏰ Daily Time Limit' },
    { value: 'digital_sunset', label: '🌅 Digital Sunset' },
    { value: 'weekend_detox', label: '🌴 Weekend Detox' },
    { value: 'focus_sessions', label: '🎯 Focus Sessions' },
  ];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content create-goal-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>🎯 Create New Goal</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="goal-form">
          <div className="form-group">
            <label>Goal Type</label>
            <select value={goalType} onChange={(e) => setGoalType(e.target.value)} required>
              {goalTypes.map((type) => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>

          {(goalType === 'reduce_total' || goalType === 'limit_daily') && (
            <div className="form-group">
              <label>Device (Optional)</label>
              <select value={deviceId} onChange={(e) => setDeviceId(e.target.value)}>
                <option value="">All Devices</option>
                {devices.map((device) => (
                  <option key={device.id} value={device.id}>
                    {device.name}
                  </option>
                ))}
              </select>
            </div>
          )}

          {(goalType === 'reduce_app' || goalType === 'increase_productive') && (
            <div className="form-group">
              <label>App</label>
              <select value={appId} onChange={(e) => setAppId(e.target.value)} required>
                <option value="">Select an app</option>
                {apps.map((app) => (
                  <option key={app.id} value={app.id}>
                    {app.display_name}
                  </option>
                ))}
              </select>
            </div>
          )}

          {(goalType.includes('reduce') || goalType === 'limit_daily' || goalType === 'increase_productive') && (
            <div className="form-group">
              <label>Target Minutes per Day</label>
              <input
                type="number"
                value={targetMinutes}
                onChange={(e) => setTargetMinutes(e.target.value)}
                placeholder="e.g., 120"
                required
              />
            </div>
          )}

          {goalType === 'digital_sunset' && (
            <div className="form-group">
              <label>Cutoff Time</label>
              <input
                type="time"
                value={cutoffTime}
                onChange={(e) => setCutoffTime(e.target.value)}
                required
              />
            </div>
          )}

          <div className="form-group">
            <label>Duration (Days)</label>
            <input
              type="number"
              value={durationDays}
              onChange={(e) => setDurationDays(e.target.value)}
              placeholder="e.g., 30"
              required
            />
          </div>

          <div className="form-group">
            <label>Notes (Optional)</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Why is this goal important to you?"
              rows={3}
            />
          </div>

          <div className="modal-footer">
            <button type="button" onClick={onClose} className="btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              Create Goal
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
