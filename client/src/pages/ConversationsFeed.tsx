import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { conversationsAPI, aiGenerationAPI } from '../services/api';
import './ConversationsFeed.css';

export default function ConversationsFeed() {
  const navigate = useNavigate();
  const [conversations, setConversations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [filter, setFilter] = useState({
    type: '',
    mood: '',
    favorites: false,
  });

  useEffect(() => {
    loadConversations();
  }, [filter]);

  const loadConversations = async () => {
    try {
      setLoading(true);
      let response;
      
      if (filter.favorites) {
        response = await conversationsAPI.favorites();
      } else {
        const params: any = {};
        if (filter.type) params.conversation_type = filter.type;
        if (filter.mood) params.mood = filter.mood;
        response = await conversationsAPI.list(params);
      }

      setConversations(response.data.results || response.data);
    } catch (error) {
      console.error('Failed to load conversations:', error);
      alert('Failed to load conversations');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (!confirm('Generate new conversations? This will create conversations based on your recent usage data.')) {
      return;
    }

    try {
      setGenerating(true);
      await aiGenerationAPI.generateForUser();
      alert('Conversations generated successfully! Refreshing...');
      await loadConversations();
    } catch (error: any) {
      console.error('Failed to generate conversations:', error);
      alert(error.response?.data?.detail || 'Failed to generate conversations. Make sure you have usage data and an OpenAI API key configured.');
    } finally {
      setGenerating(false);
    }
  };

  const handleToggleFavorite = async (id: string, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    try {
      await conversationsAPI.toggleFavorite(id);
      await loadConversations();
    } catch (error) {
      console.error('Failed to toggle favorite:', error);
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
      humorous: '😄',
      supportive: '🤗',
      dramatic: '🎭',
      sarcastic: '😏',
      philosophical: '🤔',
      worried: '😟',
      excited: '🤩',
      nostalgic: '🥲',
      passive_aggressive: '😒',
      wholesome: '🥰',
    };
    return moodMap[mood] || '💬';
  };

  const getTypeLabel = (type: string) => {
    return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  if (loading && conversations.length === 0) {
    return (
      <div className="conversations-loading">
        <div className="spinner"></div>
        <p>Loading conversations...</p>
      </div>
    );
  }

  return (
    <div className="conversations-page">
      <header className="page-header-conv">
        <div className="header-title">
          <h1>💬 Conversations</h1>
          <p>AI-generated dialogues between your devices and apps</p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="btn-generate"
        >
          {generating ? '⏳ Generating...' : '✨ Generate New'}
        </button>
      </header>

      <div className="filters">
        <div className="filter-group">
          <label>Type:</label>
          <select value={filter.type} onChange={(e) => setFilter({ ...filter, type: e.target.value })}>
            <option value="">All Types</option>
            <option value="daily_recap">Daily Recap</option>
            <option value="usage_intervention">Usage Intervention</option>
            <option value="app_drama">App Drama</option>
            <option value="morning_briefing">Morning Briefing</option>
            <option value="bedtime_review">Bedtime Review</option>
            <option value="achievement_celebration">Achievement</option>
            <option value="goal_check_in">Goal Check-in</option>
            <option value="pattern_discussion">Pattern Discussion</option>
            <option value="app_debate">App Debate</option>
            <option value="device_family_chat">Device Family</option>
            <option value="weekly_summary">Weekly Summary</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Mood:</label>
          <select value={filter.mood} onChange={(e) => setFilter({ ...filter, mood: e.target.value })}>
            <option value="">All Moods</option>
            <option value="humorous">😄 Humorous</option>
            <option value="supportive">🤗 Supportive</option>
            <option value="dramatic">🎭 Dramatic</option>
            <option value="sarcastic">😏 Sarcastic</option>
            <option value="philosophical">🤔 Philosophical</option>
            <option value="worried">😟 Worried</option>
            <option value="excited">🤩 Excited</option>
            <option value="nostalgic">🥲 Nostalgic</option>
            <option value="passive_aggressive">😒 Passive Aggressive</option>
            <option value="wholesome">🥰 Wholesome</option>
          </select>
        </div>

        <button
          className={`filter-btn ${filter.favorites ? 'active' : ''}`}
          onClick={() => setFilter({ ...filter, favorites: !filter.favorites })}
        >
          ⭐ Favorites Only
        </button>
      </div>

      {conversations.length === 0 ? (
        <div className="empty-state-conv">
          <div className="empty-icon">💬</div>
          <h3>No conversations yet</h3>
          <p>Click "Generate New" to create AI conversations based on your usage data</p>
          <button onClick={handleGenerate} className="btn-primary" disabled={generating}>
            {generating ? 'Generating...' : '✨ Generate First Conversation'}
          </button>
        </div>
      ) : (
        <div className="conversations-grid">
          {conversations.map((conv) => (
            <Link
              key={conv.id}
              to={`/conversations/${conv.id}`}
              className="conversation-card"
            >
              <div className="card-header-conv">
                <div className="conv-meta">
                  <span className="conv-mood">{getMoodEmoji(conv.mood)}</span>
                  <span className="conv-type">{getTypeLabel(conv.conversation_type)}</span>
                </div>
                <button
                  className={`favorite-btn ${conv.is_favorite ? 'active' : ''}`}
                  onClick={(e) => handleToggleFavorite(conv.id, e)}
                >
                  {conv.is_favorite ? '⭐' : '☆'}
                </button>
              </div>

              <div className="conv-content-preview">
                <p className="conv-title">{conv.title || 'Untitled Conversation'}</p>
                <p className="conv-summary">{conv.summary || 'No summary available'}</p>
              </div>

              <div className="card-footer-conv">
                <span className="conv-date">{formatDate(conv.date)}</span>
                {conv.user_rating && (
                  <span className="conv-rating">
                    {'⭐'.repeat(conv.user_rating)}
                  </span>
                )}
                {conv.participating_devices?.length > 0 && (
                  <span className="conv-participants">
                    📱 {conv.participating_devices.length} device{conv.participating_devices.length > 1 ? 's' : ''}
                  </span>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
