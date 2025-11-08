from rest_framework import serializers
from .models import FriendConnection, TemporaryDeviceConnection, Challenge
from apps.accounts.serializers import UserSerializer
from apps.devices.serializers import DeviceListSerializer


class FriendConnectionSerializer(serializers.ModelSerializer):
    friend_user_details = UserSerializer(source='friend_user', read_only=True)
    
    class Meta:
        model = FriendConnection
        fields = [
            'id', 'user', 'friend_user', 'friend_user_details',
            'is_active', 'can_compare_stats', 'can_see_conversations',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TemporaryDeviceConnectionSerializer(serializers.ModelSerializer):
    visitor_device_details = DeviceListSerializer(source='visitor_device', read_only=True)
    host_user_details = UserSerializer(source='host_user', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = TemporaryDeviceConnection
        fields = [
            'id', 'host_user', 'host_user_details', 'visitor_user',
            'visitor_device', 'visitor_device_details', 'connection_name',
            'expires_at', 'is_active', 'is_expired',
            'can_participate_in_conversations', 'can_see_usage_stats',
            'created_at', 'activated_at'
        ]
        read_only_fields = ['id', 'created_at', 'activated_at', 'is_expired']


class ChallengeSerializer(serializers.ModelSerializer):
    creator_details = UserSerializer(source='creator', read_only=True)
    participants_details = UserSerializer(source='participants', many=True, read_only=True)
    winner_details = UserSerializer(source='winner', read_only=True)
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'creator', 'creator_details', 'participants',
            'participants_details', 'title', 'description',
            'challenge_type', 'start_date', 'end_date', 'duration_days',
            'target_metric', 'target_value', 'is_active',
            'winner', 'winner_details', 'created_at'
        ]
        read_only_fields = ['id', 'creator', 'created_at']
    
    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)
