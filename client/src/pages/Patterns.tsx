import { useState, useEffect } from 'react';
import { patternsAPI } from '../services/api';
import './Patterns.css';

interface Pattern {
  id: string;
  pattern_type: string;
  description: string;
  confidence_score: number;
  start_date: string;
  end_date?: string;
  days_observed: number;
  frequency: string;
  strength: string;
  impact_on_productivity: number;
  impact_on_wellness: number;
  is_active: boolean;
  user_acknowledged: boolean;
  device?: { id: string; name: string };
  apps_involved?: Array<{ id: string; display_name: string }>;
  pattern_data?: any;
}

export default function Patterns() {
  const [patterns, setPatterns] = useState<Pattern[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'active' | 'acknowledged'>('active');
  const [selectedPattern, setSelectedPattern] = useState<Pattern | null>(null);

  useEffect(() => {
    loadPatterns();
  }, []);

  const loadPatterns = async () => {
    try {
      const response = await patternsAPI.list();
      setPatterns(response.data.results || response.data || []);
    } catch (error) {
      console.error('Failed to load patterns:', error);
    } finally {
      setLoading(false);
    }
  };

  const getPatternIcon = (type: string) => {
    const icons: Record<string, string> = {
      binge_usage: '🍿',
      night_owl: '🦉',
      morning_person: '🌅',
      weekend_warrior: '🏖️',
      distracted: '😵',
      doom_scrolling: '📜',
      phantom_vibration: '📳',
      app_switching: '🔀',
      notification_addiction: '🔔',
    };
    return icons[type] || '📊';
  };

  const getPatternLabel = (type: string) => {
    const labels: Record<string, string> = {
      binge_usage: 'Binge Usage',
      night_owl: 'Night Owl',
      morning_person: 'Morning Person',
      weekend_warrior: 'Weekend Warrior',
      distracted: 'Distracted',
      doom_scrolling: 'Doom Scrolling',
      phantom_vibration: 'Phantom Vibration',
      app_switching: 'App Switching',
      notification_addiction: 'Notification Addiction',
    };
    return labels[type] || type.replace('_', ' ');
  };

  const getStrengthColor = (strength: string) => {
    const colors: Record<string, string> = {
      weak: '#94a3b8',
      moderate: '#f59e0b',
      strong: '#ef4444',
      very_strong: '#dc2626',
    };
    return colors[strength] || '#94a3b8';
  };

  const getImpactColor = (impact: number) => {
    if (impact <= -3) return '#dc2626'; // Very negative
    if (impact <= -1) return '#f59e0b'; // Negative
    if (impact <= 1) return '#94a3b8'; // Neutral
    if (impact <= 3) return '#10b981'; // Positive
    return '#059669'; // Very positive
  };

  const getConfidenceLabel = (score: number) => {
    if (score >= 0.9) return 'Very High';
    if (score >= 0.7) return 'High';
    if (score >= 0.5) return 'Medium';
    return 'Low';
  };

  const filteredPatterns = patterns.filter((pattern) => {
    if (filter === 'active') return pattern.is_active;
    if (filter === 'acknowledged') return pattern.user_acknowledged;
    return true;
  });

  if (loading) {
    return (
      <div className="patterns-loading">
        <div className="spinner"></div>
        <p>Analyzing your usage patterns...</p>
      </div>
    );
  }

  return (
    <div className="patterns-page">
      <header className="patterns-header">
        <div className="header-content">
          <h1>📊 Usage Patterns</h1>
          <p className="subtitle">AI-detected patterns in your digital behavior</p>
        </div>
      </header>

      <div className="patterns-filters">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Patterns
        </button>
        <button
          className={`filter-btn ${filter === 'active' ? 'active' : ''}`}
          onClick={() => setFilter('active')}
        >
          Active
        </button>
        <button
          className={`filter-btn ${filter === 'acknowledged' ? 'active' : ''}`}
          onClick={() => setFilter('acknowledged')}
        >
          Acknowledged
        </button>
      </div>

      {filteredPatterns.length === 0 ? (
        <div className="patterns-empty">
          <div className="empty-icon">📊</div>
          <h3>No patterns detected yet</h3>
          <p>Keep using the app and we'll start detecting patterns in your usage!</p>
        </div>
      ) : (
        <div className="patterns-grid">
          {filteredPatterns.map((pattern) => (
            <div
              key={pattern.id}
              className={`pattern-card ${!pattern.is_active ? 'inactive' : ''}`}
              onClick={() => setSelectedPattern(pattern)}
            >
              <div className="pattern-header">
                <div className="pattern-type">
                  <span className="pattern-icon">{getPatternIcon(pattern.pattern_type)}</span>
                  <div>
                    <h3>{getPatternLabel(pattern.pattern_type)}</h3>
                    {pattern.device && (
                      <span className="pattern-device">on {pattern.device.name}</span>
                    )}
                  </div>
                </div>
                <div
                  className="strength-badge"
                  style={{ background: getStrengthColor(pattern.strength) }}
                >
                  {pattern.strength.replace('_', ' ')}
                </div>
              </div>

              <p className="pattern-description">{pattern.description}</p>

              <div className="pattern-meta">
                <div className="meta-item">
                  <span className="meta-label">Confidence</span>
                  <span className="meta-value">
                    {getConfidenceLabel(pattern.confidence_score)} ({(pattern.confidence_score * 100).toFixed(0)}%)
                  </span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Frequency</span>
                  <span className="meta-value">{pattern.frequency}</span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Observed</span>
                  <span className="meta-value">{pattern.days_observed} days</span>
                </div>
              </div>

              <div className="impact-indicators">
                <div className="impact">
                  <span className="impact-label">Productivity Impact</span>
                  <div className="impact-bar">
                    <div
                      className="impact-fill"
                      style={{
                        width: `${Math.abs(pattern.impact_on_productivity) * 10}%`,
                        background: getImpactColor(pattern.impact_on_productivity),
                      }}
                    />
                  </div>
                  <span className="impact-value">{pattern.impact_on_productivity}/5</span>
                </div>
                <div className="impact">
                  <span className="impact-label">Wellness Impact</span>
                  <div className="impact-bar">
                    <div
                      className="impact-fill"
                      style={{
                        width: `${Math.abs(pattern.impact_on_wellness) * 10}%`,
                        background: getImpactColor(pattern.impact_on_wellness),
                      }}
                    />
                  </div>
                  <span className="impact-value">{pattern.impact_on_wellness}/5</span>
                </div>
              </div>

              {pattern.apps_involved && pattern.apps_involved.length > 0 && (
                <div className="apps-involved">
                  <strong>Apps:</strong>
                  {pattern.apps_involved.slice(0, 3).map((app) => (
                    <span key={app.id} className="app-tag">
                      {app.display_name}
                    </span>
                  ))}
                  {pattern.apps_involved.length > 3 && (
                    <span className="app-tag">+{pattern.apps_involved.length - 3} more</span>
                  )}
                </div>
              )}

              <div className="pattern-footer">
                <span className="pattern-dates">
                  {new Date(pattern.start_date).toLocaleDateString()}
                  {pattern.end_date && ` - ${new Date(pattern.end_date).toLocaleDateString()}`}
                  {!pattern.end_date && ' - Ongoing'}
                </span>
                {pattern.user_acknowledged && (
                  <span className="acknowledged-badge">✓ Acknowledged</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedPattern && (
        <PatternDetailModal
          pattern={selectedPattern}
          onClose={() => setSelectedPattern(null)}
        />
      )}
    </div>
  );
}

interface PatternDetailModalProps {
  pattern: Pattern;
  onClose: () => void;
}

function PatternDetailModal({ pattern, onClose }: PatternDetailModalProps) {
  const getPatternIcon = (type: string) => {
    const icons: Record<string, string> = {
      binge_usage: '🍿',
      night_owl: '🦉',
      morning_person: '🌅',
      weekend_warrior: '🏖️',
      distracted: '😵',
      doom_scrolling: '📜',
      phantom_vibration: '📳',
      app_switching: '🔀',
      notification_addiction: '🔔',
    };
    return icons[type] || '📊';
  };

  const getPatternLabel = (type: string) => {
    const labels: Record<string, string> = {
      binge_usage: 'Binge Usage',
      night_owl: 'Night Owl',
      morning_person: 'Morning Person',
      weekend_warrior: 'Weekend Warrior',
      distracted: 'Distracted',
      doom_scrolling: 'Doom Scrolling',
      phantom_vibration: 'Phantom Vibration',
      app_switching: 'App Switching',
      notification_addiction: 'Notification Addiction',
    };
    return labels[type] || type.replace('_', ' ');
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content pattern-detail-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <span className="modal-icon">{getPatternIcon(pattern.pattern_type)}</span>
            <h2>{getPatternLabel(pattern.pattern_type)}</h2>
          </div>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          <section className="detail-section">
            <h3>Description</h3>
            <p>{pattern.description}</p>
          </section>

          {pattern.device && (
            <section className="detail-section">
              <h3>Device</h3>
              <p>{pattern.device.name}</p>
            </section>
          )}

          <section className="detail-section">
            <h3>Pattern Metrics</h3>
            <div className="metrics-grid">
              <div className="metric">
                <span className="metric-label">Strength</span>
                <span className="metric-value">{pattern.strength.replace('_', ' ')}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Confidence</span>
                <span className="metric-value">{(pattern.confidence_score * 100).toFixed(0)}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Frequency</span>
                <span className="metric-value">{pattern.frequency}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Days Observed</span>
                <span className="metric-value">{pattern.days_observed}</span>
              </div>
            </div>
          </section>

          <section className="detail-section">
            <h3>Impact Assessment</h3>
            <div className="impact-details">
              <div className="impact-item">
                <span className="impact-label">Productivity Impact</span>
                <div className="impact-visual">
                  <div className="impact-scale">
                    {[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5].map((val) => (
                      <div
                        key={val}
                        className={`scale-tick ${val === pattern.impact_on_productivity ? 'active' : ''}`}
                      />
                    ))}
                  </div>
                  <span className="impact-number">{pattern.impact_on_productivity}/5</span>
                </div>
              </div>
              <div className="impact-item">
                <span className="impact-label">Wellness Impact</span>
                <div className="impact-visual">
                  <div className="impact-scale">
                    {[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5].map((val) => (
                      <div
                        key={val}
                        className={`scale-tick ${val === pattern.impact_on_wellness ? 'active' : ''}`}
                      />
                    ))}
                  </div>
                  <span className="impact-number">{pattern.impact_on_wellness}/5</span>
                </div>
              </div>
            </div>
          </section>

          {pattern.apps_involved && pattern.apps_involved.length > 0 && (
            <section className="detail-section">
              <h3>Apps Involved</h3>
              <div className="apps-list">
                {pattern.apps_involved.map((app) => (
                  <span key={app.id} className="app-chip">
                    {app.display_name}
                  </span>
                ))}
              </div>
            </section>
          )}

          {pattern.pattern_data && Object.keys(pattern.pattern_data).length > 0 && (
            <section className="detail-section">
              <h3>Additional Data</h3>
              <pre className="pattern-data">{JSON.stringify(pattern.pattern_data, null, 2)}</pre>
            </section>
          )}

          <section className="detail-section">
            <h3>Timeline</h3>
            <p>
              <strong>Started:</strong> {new Date(pattern.start_date).toLocaleDateString()}
              <br />
              {pattern.end_date ? (
                <>
                  <strong>Ended:</strong> {new Date(pattern.end_date).toLocaleDateString()}
                </>
              ) : (
                <span className="ongoing-badge">Ongoing</span>
              )}
            </p>
          </section>
        </div>

        <div className="modal-footer">
          <button onClick={onClose} className="btn-primary">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
