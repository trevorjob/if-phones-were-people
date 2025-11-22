import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { devicesAPI } from '../services/api';
import './DeviceCard.css';

interface DeviceCardProps {
  device: any;
  onDeleted: () => void;
}

export default function DeviceCard({ device, onDeleted }: DeviceCardProps) {
  const navigate = useNavigate();
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async () => {
    if (!confirm(`Are you sure you want to delete ${device.name}?`)) {
      return;
    }

    setDeleting(true);
    try {
      await devicesAPI.delete(device.id);
      onDeleted();
    } catch (error) {
      console.error('Failed to delete device:', error);
      alert('Failed to delete device');
      setDeleting(false);
    }
  };

  const getPersonalityEmoji = (personality: string) => {
    const emojiMap: Record<string, string> = {
      snarky: '😏',
      logical: '🤖',
      chaotic: '🌀',
      supportive: '🤗',
      dramatic: '🎭',
      minimalist: '⬜',
      workaholic: '💼',
      social: '👥',
      creative: '🎨',
      anxious: '😰',
      chill: '😎',
      competitive: '🏆',
    };
    return emojiMap[personality] || '📱';
  };

  const getPlatformIcon = (platform: string) => {
    const iconMap: Record<string, string> = {
      ios: '🍎',
      android: '🤖',
      windows: '🪟',
      macos: '💻',
      linux: '🐧',
      web: '🌐',
    };
    return iconMap[platform] || '📱';
  };

  return (
    <div className="device-card">
      <div className="device-icon">
        {device.device_type?.icon || '📱'}
      </div>

      <div className="device-info">
        <h3>{device.name}</h3>
        <p className="device-model">
          {getPlatformIcon(device.platform)} {device.model_name || device.platform}
        </p>
        <div className="device-personality">
          {getPersonalityEmoji(device.personality_type)} {device.personality_type}
        </div>
        <div className="device-status">
          <span className={`status-badge ${device.is_active ? 'active' : 'inactive'}`}>
            {device.is_active ? '✓ Active' : '○ Inactive'}
          </span>
        </div>
      </div>

      <div className="device-actions">
        <button
          onClick={() => navigate(`/device/${device.id}`)}
          className="btn-action btn-view"
        >
          View Details
        </button>
        <button
          onClick={() => navigate(`/device/${device.id}/usage`)}
          className="btn-action btn-usage"
        >
          Add Usage
        </button>
        <button
          onClick={handleDelete}
          className="btn-action btn-delete"
          disabled={deleting}
        >
          {deleting ? 'Deleting...' : 'Delete'}
        </button>
      </div>
    </div>
  );
}
