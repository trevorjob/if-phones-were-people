import { useState, useEffect } from 'react';
import { analyticsAPI, patternsAPI } from '../services/api';
import './Analytics.css';

export default function Analytics() {
  const [stats, setStats] = useState<any>(null);
  const [trends, setTrends] = useState<any>(null);
  const [patterns, setPatterns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [periodType, setPeriodType] = useState('weekly');

  useEffect(() => {
    loadAnalytics();
  }, [periodType]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const [statsRes, trendsRes, patternsRes] = await Promise.all([
        analyticsAPI.stats.latest(),
        analyticsAPI.trends.latest(periodType),
        patternsAPI.list({ is_active: true }),
      ]);

      setStats(statsRes.data);
      setTrends(trendsRes.data);
      setPatterns(patternsRes.data.results || patternsRes.data);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const getWellnessColor = (score: number) => {
    if (score >= 80) return '#10b981'; // green
    if (score >= 60) return '#f59e0b'; // amber
    if (score >= 40) return '#f97316'; // orange
    return '#ef4444'; // red
  };

  const getWellnessLabel = (score: number) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Needs Attention';
  };

  const formatMinutes = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
  };

  const getPatternIcon = (type: string) => {
    const icons: any = {
      binge_usage: '📺',
      night_owl: '🦉',
      morning_person: '🌅',
      weekend_warrior: '🎉',
      distracted: '🤯',
      doom_scrolling: '📱',
      phantom_vibration: '📳',
      app_switching: '🔄',
      notification_addiction: '🔔',
    };
    return icons[type] || '📊';
  };

  if (loading) {
    return (
      <div className="analytics-loading">
        <div className="spinner"></div>
        <p>Loading analytics...</p>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="analytics-empty">
        <div className="empty-icon">📊</div>
        <h3>No analytics data yet</h3>
        <p>Start tracking your usage to see insights and analytics</p>
      </div>
    );
  }

  return (
    <div className="analytics-page">
      <header className="analytics-header">
        <div>
          <h1>📊 Analytics & Insights</h1>
          <p>Your digital wellness dashboard</p>
        </div>
      </header>

      {/* Wellness Score */}
      <div className="wellness-section">
        <div className="wellness-card">
          <div className="wellness-header">
            <h2>Wellness Score</h2>
            <span className="wellness-period">{periodType}</span>
          </div>
          <div className="wellness-score-display">
            <div 
              className="score-circle"
              style={{ 
                background: `conic-gradient(${getWellnessColor(stats.wellness_score)} ${stats.wellness_score * 3.6}deg, #f0f0f0 0deg)`
              }}
            >
              <div className="score-inner">
                <span className="score-number">{stats.wellness_score}</span>
                <span className="score-label">{getWellnessLabel(stats.wellness_score)}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="quick-stats-grid">
          <div className="stat-card">
            <div className="stat-icon">⏱️</div>
            <div className="stat-content">
              <p className="stat-label">Avg Screen Time</p>
              <p className="stat-value">{formatMinutes(stats.average_screen_time_minutes || 0)}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🔓</div>
            <div className="stat-content">
              <p className="stat-label">Avg Unlocks</p>
              <p className="stat-value">{Math.round(stats.average_unlocks || 0)}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📱</div>
            <div className="stat-content">
              <p className="stat-label">Avg Pickups</p>
              <p className="stat-value">{Math.round(stats.average_pickups || 0)}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🔔</div>
            <div className="stat-content">
              <p className="stat-label">Avg Notifications</p>
              <p className="stat-value">{Math.round(stats.average_notifications || 0)}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🔥</div>
            <div className="stat-content">
              <p className="stat-label">Current Streak</p>
              <p className="stat-value">{stats.current_streak || 0} days</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🏆</div>
            <div className="stat-content">
              <p className="stat-label">Best Streak</p>
              <p className="stat-value">{stats.best_streak || 0} days</p>
            </div>
          </div>
        </div>
      </div>

      {/* Trends */}
      {trends && (
        <div className="trends-section">
          <div className="section-header">
            <h2>📈 Trends</h2>
            <div className="period-selector">
              <button
                className={periodType === 'weekly' ? 'active' : ''}
                onClick={() => setPeriodType('weekly')}
              >
                Weekly
              </button>
              <button
                className={periodType === 'monthly' ? 'active' : ''}
                onClick={() => setPeriodType('monthly')}
              >
                Monthly
              </button>
            </div>
          </div>

          <div className="trends-grid">
            {trends.popular_apps && trends.popular_apps.length > 0 && (
              <div className="trend-card">
                <h3>📲 Most Used Apps</h3>
                <div className="app-list">
                  {trends.popular_apps.slice(0, 5).map((app: any, index: number) => (
                    <div key={index} className="app-item-trend">
                      <span className="app-rank">#{index + 1}</span>
                      <span className="app-name">{app.app_name}</span>
                      <span className="app-time">{formatMinutes(app.total_time)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {trends.usage_patterns && trends.usage_patterns.length > 0 && (
              <div className="trend-card">
                <h3>🔍 Usage Patterns</h3>
                <div className="patterns-list">
                  {trends.usage_patterns.map((pattern: string, index: number) => (
                    <div key={index} className="pattern-badge">
                      {pattern}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {trends.peak_usage_hours && trends.peak_usage_hours.length > 0 && (
              <div className="trend-card">
                <h3>⏰ Peak Usage Hours</h3>
                <div className="hours-list">
                  {trends.peak_usage_hours.map((hour: number, index: number) => (
                    <span key={index} className="hour-badge">
                      {hour}:00
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Active Patterns */}
      {patterns.length > 0 && (
        <div className="patterns-section">
          <h2>🔍 Detected Patterns</h2>
          <div className="patterns-grid">
            {patterns.map((pattern) => (
              <div key={pattern.id} className="pattern-card">
                <div className="pattern-header">
                  <span className="pattern-icon">{getPatternIcon(pattern.pattern_type)}</span>
                  <h3>{pattern.pattern_type.replace(/_/g, ' ')}</h3>
                </div>
                <p className="pattern-description">{pattern.description}</p>
                <div className="pattern-meta">
                  <span className="pattern-confidence">
                    Confidence: {Math.round(pattern.confidence_score * 100)}%
                  </span>
                  <span className="pattern-frequency">
                    {pattern.frequency}
                  </span>
                </div>
                {pattern.impact_on_wellness && (
                  <div className="pattern-impact">
                    <span>Impact: {pattern.impact_on_wellness}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
