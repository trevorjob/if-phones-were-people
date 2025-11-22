import { useState, useEffect } from 'react';
import { journalsAPI, aiGenerationAPI } from '../services/api';
import './Journals.css';

type JournalType = 'device' | 'app';

export default function Journals() {
  const [journalType, setJournalType] = useState<JournalType>('device');
  const [journals, setJournals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [selectedJournal, setSelectedJournal] = useState<any>(null);

  useEffect(() => {
    loadJournals();
  }, [journalType]);

  const loadJournals = async () => {
    try {
      setLoading(true);
      let response;
      
      if (journalType === 'device') {
        response = await journalsAPI.deviceJournals.list();
      } else {
        response = await journalsAPI.appJournals.list();
      }

      setJournals(response.data.results || response.data);
    } catch (error) {
      console.error('Failed to load journals:', error);
      alert('Failed to load journals');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (!confirm('Generate new journals? This will create journal entries based on your recent usage data.')) {
      return;
    }

    try {
      setGenerating(true);
      await aiGenerationAPI.generateJournals();
      alert('Journals generated successfully! Refreshing...');
      await loadJournals();
    } catch (error: any) {
      console.error('Failed to generate journals:', error);
      alert(error.response?.data?.detail || 'Failed to generate journals. Make sure you have usage data and an OpenAI API key configured.');
    } finally {
      setGenerating(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getMoodEmoji = (mood: string) => {
    const moodMap: any = {
      happy: '😊',
      sad: '😢',
      excited: '🤩',
      anxious: '😰',
      proud: '😎',
      overwhelmed: '😵',
      content: '😌',
      frustrated: '😤',
      curious: '🤔',
      grateful: '🙏',
    };
    return moodMap[mood] || '😐';
  };

  if (loading && journals.length === 0) {
    return (
      <div className="journals-loading">
        <div className="spinner"></div>
        <p>Loading journals...</p>
      </div>
    );
  }

  return (
    <div className="journals-page">
      <header className="journals-header">
        <div className="header-title">
          <h1>📔 Journals</h1>
          <p>First-person diary entries from your devices and apps</p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="btn-generate"
        >
          {generating ? '⏳ Generating...' : '✨ Generate New'}
        </button>
      </header>

      <div className="journal-type-tabs">
        <button
          className={`tab ${journalType === 'device' ? 'active' : ''}`}
          onClick={() => setJournalType('device')}
        >
          📱 Device Journals
        </button>
        <button
          className={`tab ${journalType === 'app' ? 'active' : ''}`}
          onClick={() => setJournalType('app')}
        >
          📲 App Journals
        </button>
      </div>

      {journals.length === 0 ? (
        <div className="empty-state-journals">
          <div className="empty-icon">📔</div>
          <h3>No journals yet</h3>
          <p>Click "Generate New" to create {journalType === 'device' ? 'device' : 'app'} journal entries</p>
          <button onClick={handleGenerate} className="btn-primary" disabled={generating}>
            {generating ? 'Generating...' : '✨ Generate First Journal'}
          </button>
        </div>
      ) : (
        <div className="journals-layout">
          <div className="journals-list">
            {journals.map((journal) => (
              <div
                key={journal.id}
                className={`journal-item ${selectedJournal?.id === journal.id ? 'active' : ''}`}
                onClick={() => setSelectedJournal(journal)}
              >
                <div className="journal-item-header">
                  <span className="journal-mood">{getMoodEmoji(journal.mood)}</span>
                  <div className="journal-item-info">
                    <h3 className="journal-item-title">
                      {journalType === 'device' 
                        ? journal.device?.name 
                        : journal.device_app?.custom_name || journal.device_app?.app?.name}
                    </h3>
                    <span className="journal-item-date">{formatDate(journal.date)}</span>
                  </div>
                </div>
                <p className="journal-preview">
                  {journal.content?.substring(0, 100)}...
                </p>
                {journal.notable_events?.length > 0 && (
                  <div className="journal-events-preview">
                    <span className="events-count">
                      {journal.notable_events.length} event{journal.notable_events.length > 1 ? 's' : ''}
                    </span>
                  </div>
                )}
              </div>
            ))}
          </div>

          {selectedJournal && (
            <div className="journal-detail">
              <div className="journal-detail-header">
                <div>
                  <div className="mood-badge">
                    {getMoodEmoji(selectedJournal.mood)} {selectedJournal.mood}
                  </div>
                  <h2>
                    {journalType === 'device'
                      ? selectedJournal.device?.name
                      : selectedJournal.device_app?.custom_name || selectedJournal.device_app?.app?.name}
                  </h2>
                  <p className="detail-date">{formatDate(selectedJournal.date)}</p>
                </div>
              </div>

              <div className="journal-content">
                <pre className="journal-text">{selectedJournal.content}</pre>
              </div>

              {selectedJournal.notable_events?.length > 0 && (
                <div className="notable-events">
                  <h3>Notable Events</h3>
                  <ul className="events-list">
                    {selectedJournal.notable_events.map((event: string, index: number) => (
                      <li key={index}>{event}</li>
                    ))}
                  </ul>
                </div>
              )}

              {selectedJournal.mentioned_apps?.length > 0 && (
                <div className="mentioned-apps">
                  <h3>Apps Mentioned</h3>
                  <div className="apps-tags">
                    {selectedJournal.mentioned_apps.map((app: any) => (
                      <span key={app.id} className="app-tag">
                        {app.custom_name || app.app?.name}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {selectedJournal.mentioned_devices?.length > 0 && (
                <div className="mentioned-devices">
                  <h3>Devices Mentioned</h3>
                  <div className="devices-tags">
                    {selectedJournal.mentioned_devices.map((device: any) => (
                      <span key={device.id} className="device-tag">
                        {device.name}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {!selectedJournal && journals.length > 0 && (
            <div className="journal-detail-placeholder">
              <div className="placeholder-icon">📔</div>
              <p>Select a journal entry to read</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
