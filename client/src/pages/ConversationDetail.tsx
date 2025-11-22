import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { conversationsAPI } from '../services/api';
import './ConversationDetail.css';

export default function ConversationDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [conversation, setConversation] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [rating, setRating] = useState(0);
  const [feedback, setFeedback] = useState('');
  const [showRating, setShowRating] = useState(false);

  useEffect(() => {
    loadConversation();
  }, [id]);

  const loadConversation = async () => {
    try {
      const response = await conversationsAPI.get(id!);
      setConversation(response.data);
      setRating(response.data.user_rating || 0);
    } catch (error) {
      console.error('Failed to load conversation:', error);
      alert('Failed to load conversation');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleFavorite = async () => {
    try {
      await conversationsAPI.toggleFavorite(id!);
      await loadConversation();
    } catch (error) {
      console.error('Failed to toggle favorite:', error);
    }
  };

  const handleSubmitRating = async () => {
    try {
      await conversationsAPI.rate(id!, rating, feedback);
      setShowRating(false);
      await loadConversation();
      alert('Rating submitted!');
    } catch (error) {
      console.error('Failed to submit rating:', error);
      alert('Failed to submit rating');
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'long',
      month: 'long',
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

  if (loading) {
    return (
      <div className="detail-loading">
        <div className="spinner"></div>
        <p>Loading conversation...</p>
      </div>
    );
  }

  if (!conversation) {
    return (
      <div className="detail-error">
        <p>Conversation not found</p>
        <button onClick={() => navigate('/conversations')} className="btn-secondary">
          Back to Conversations
        </button>
      </div>
    );
  }

  return (
    <div className="conversation-detail-page">
      <header className="detail-header">
        <button onClick={() => navigate('/conversations')} className="back-btn">
          ← Back
        </button>
        <div className="header-actions">
          <button onClick={handleToggleFavorite} className="icon-btn">
            {conversation.is_favorite ? '⭐' : '☆'}
          </button>
          <button onClick={() => setShowRating(!showRating)} className="icon-btn">
            👍 Rate
          </button>
        </div>
      </header>

      <div className="detail-container">
        <div className="detail-header-info">
          <div className="mood-badge">
            {getMoodEmoji(conversation.mood)} {conversation.mood}
          </div>
          <h1>{conversation.title || 'Untitled Conversation'}</h1>
          <div className="detail-meta">
            <span className="meta-item">
              📅 {formatDate(conversation.date)}
            </span>
            <span className="meta-item">
              🏷️ {conversation.conversation_type.replace(/_/g, ' ')}
            </span>
            {conversation.participating_devices?.length > 0 && (
              <span className="meta-item">
                📱 {conversation.participating_devices.length} device(s)
              </span>
            )}
            {conversation.participating_apps?.length > 0 && (
              <span className="meta-item">
                📲 {conversation.participating_apps.length} app(s)
              </span>
            )}
          </div>
        </div>

        {showRating && (
          <div className="rating-panel">
            <h3>Rate this conversation</h3>
            <div className="star-rating">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => setRating(star)}
                  className={`star ${star <= rating ? 'active' : ''}`}
                >
                  ⭐
                </button>
              ))}
            </div>
            <textarea
              placeholder="Optional feedback..."
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              className="feedback-input"
            />
            <div className="rating-actions">
              <button onClick={handleSubmitRating} className="btn-primary">
                Submit Rating
              </button>
              <button onClick={() => setShowRating(false)} className="btn-secondary">
                Cancel
              </button>
            </div>
          </div>
        )}

        {conversation.summary && (
          <div className="summary-section">
            <h3>Summary</h3>
            <p>{conversation.summary}</p>
          </div>
        )}

        <div className="conversation-content">
          <h3>Conversation</h3>
          <div className="content-text">
            {conversation.content ? (
              <pre className="conversation-text">{conversation.content}</pre>
            ) : (
              <p className="no-content">No conversation content available</p>
            )}
          </div>
        </div>

        {conversation.key_topics?.length > 0 && (
          <div className="topics-section">
            <h3>Topics Discussed</h3>
            <div className="topics-tags">
              {conversation.key_topics.map((topic: string, index: number) => (
                <span key={index} className="topic-tag">
                  {topic}
                </span>
              ))}
            </div>
          </div>
        )}

        {conversation.user_rating && (
          <div className="existing-rating">
            <h3>Your Rating</h3>
            <div className="rating-display">
              {'⭐'.repeat(conversation.user_rating)}
              <span className="rating-number">({conversation.user_rating}/5)</span>
            </div>
            {conversation.user_feedback && (
              <p className="user-feedback">{conversation.user_feedback}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
