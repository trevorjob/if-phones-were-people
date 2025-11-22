import { useState } from 'react';
import { devicesAPI } from '../services/api';
import './AddDevice.css';

interface AddDeviceProps {
  deviceTypes: any[];
  personalityTraits: any[];
  onClose: () => void;
  onAdded: () => void;
}

export default function AddDevice({ deviceTypes, personalityTraits, onClose, onAdded }: AddDeviceProps) {
  const [formData, setFormData] = useState({
    name: '',
    device_type: '',
    platform: 'ios',
    model_name: '',
    personality_type: 'social',
    personality_traits: [] as number[],
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await devicesAPI.create(formData);
      onAdded();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add device');
    } finally {
      setLoading(false);
    }
  };

  const toggleTrait = (traitId: number) => {
    setFormData({
      ...formData,
      personality_traits: formData.personality_traits.includes(traitId)
        ? formData.personality_traits.filter(id => id !== traitId)
        : [...formData.personality_traits, traitId]
    });
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Add New Device</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Device Name *</label>
            <input
              id="name"
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g., My iPhone"
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="device_type">Device Type *</label>
              <select
                id="device_type"
                value={formData.device_type}
                onChange={(e) => setFormData({ ...formData, device_type: e.target.value })}
                required
              >
                <option value="">Select type...</option>
                {deviceTypes.map((type) => (
                  <option key={type.id} value={type.id}>
                    {type.icon} {type.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="platform">Platform *</label>
              <select
                id="platform"
                value={formData.platform}
                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                required
              >
                <option value="ios">iOS</option>
                <option value="android">Android</option>
                <option value="windows">Windows</option>
                <option value="macos">macOS</option>
                <option value="linux">Linux</option>
                <option value="web">Web Browser</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="model_name">Model Name</label>
            <input
              id="model_name"
              type="text"
              value={formData.model_name}
              onChange={(e) => setFormData({ ...formData, model_name: e.target.value })}
              placeholder="e.g., iPhone 15 Pro"
            />
          </div>

          <div className="form-group">
            <label htmlFor="personality_type">Primary Personality *</label>
            <select
              id="personality_type"
              value={formData.personality_type}
              onChange={(e) => setFormData({ ...formData, personality_type: e.target.value })}
              required
            >
              <option value="snarky">😏 Snarky</option>
              <option value="logical">🤖 Logical</option>
              <option value="chaotic">🌀 Chaotic</option>
              <option value="supportive">🤗 Supportive</option>
              <option value="dramatic">🎭 Dramatic</option>
              <option value="minimalist">⬜ Minimalist</option>
              <option value="workaholic">💼 Workaholic</option>
              <option value="social">👥 Social Butterfly</option>
              <option value="creative">🎨 Creative</option>
              <option value="anxious">😰 Anxious</option>
              <option value="chill">😎 Chill</option>
              <option value="competitive">🏆 Competitive</option>
            </select>
          </div>

          <div className="form-group">
            <label>Additional Personality Traits (Optional)</label>
            <div className="traits-grid">
              {personalityTraits.map((trait) => (
                <button
                  key={trait.id}
                  type="button"
                  className={`trait-chip ${formData.personality_traits.includes(trait.id) ? 'active' : ''}`}
                  onClick={() => toggleTrait(trait.id)}
                >
                  {trait.name}
                </button>
              ))}
            </div>
          </div>

          <div className="modal-actions">
            <button type="button" onClick={onClose} className="btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Adding...' : 'Add Device'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
