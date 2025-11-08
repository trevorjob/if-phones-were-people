from rest_framework import serializers
from .models import (
    Conversation, ConversationTrigger, DeviceJournal, AppJournal,
    ConversationTemplate, ConversationFeedback
)
from apps.devices.serializers import DeviceListSerializer
from apps.applications.serializers import DeviceAppListSerializer


class ConversationTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationTrigger
        fields = [
            'id', 'name', 'description', 'trigger_type', 'conditions',
            'priority', 'cooldown_hours', 'is_active'
        ]
        read_only_fields = ['id']


class ConversationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    participant_count = serializers.IntegerField(read_only=True)
    word_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'title', 'date', 'conversation_type', 'mood',
            'participant_count', 'word_count', 'user_rating',
            'is_favorite', 'is_hidden', 'generation_status',
            'created_at'
        ]
        read_only_fields = ['id', 'participant_count', 'word_count', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Full serializer with all details"""
    participating_devices_details = DeviceListSerializer(source='participating_devices', many=True, read_only=True)
    participating_apps_details = DeviceAppListSerializer(source='participating_apps', many=True, read_only=True)
    triggers_details = ConversationTriggerSerializer(source='triggers', many=True, read_only=True)
    participant_count = serializers.IntegerField(read_only=True)
    word_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'user', 'title', 'date', 'conversation_type',
            'participating_devices', 'participating_devices_details',
            'participating_apps', 'participating_apps_details',
            'guest_devices', 'content', 'summary', 'mood',
            'triggers', 'triggers_details', 'trigger_data',
            'ai_model_used', 'generation_prompt', 'generation_tokens',
            'generation_cost', 'user_rating', 'user_feedback',
            'is_favorite', 'is_hidden', 'generation_status',
            'participant_count', 'word_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'participant_count', 'word_count', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DeviceJournalSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    mentioned_apps_details = DeviceAppListSerializer(source='mentioned_apps', many=True, read_only=True)
    mentioned_devices_details = DeviceListSerializer(source='mentioned_devices', many=True, read_only=True)
    
    class Meta:
        model = DeviceJournal
        fields = [
            'id', 'device', 'device_name', 'date', 'content', 'mood',
            'notable_events', 'insights', 'mentioned_apps',
            'mentioned_apps_details', 'mentioned_devices',
            'mentioned_devices_details', 'usage_summary',
            'personality_development', 'ai_generated', 'generation_prompt',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        device = attrs.get('device')
        user = self.context['request'].user
        
        if device.user != user:
            raise serializers.ValidationError("This device does not belong to you")
        
        return attrs


class AppJournalSerializer(serializers.ModelSerializer):
    app_name = serializers.CharField(source='device_app.display_name', read_only=True)
    mentioned_apps_details = DeviceAppListSerializer(source='mentioned_apps', many=True, read_only=True)
    
    class Meta:
        model = AppJournal
        fields = [
            'id', 'device_app', 'app_name', 'date', 'content', 'mood',
            'session_highlights', 'user_behavior_notes', 'app_interactions',
            'mentioned_apps', 'mentioned_apps_details',
            'usage_satisfaction', 'productivity_contribution',
            'ai_generated', 'generation_prompt', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        device_app = attrs.get('device_app')
        user = self.context['request'].user
        
        if device_app.device.user != user:
            raise serializers.ValidationError("This app does not belong to your devices")
        
        return attrs


class ConversationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationTemplate
        fields = [
            'id', 'name', 'conversation_type', 'system_prompt',
            'user_prompt_template', 'max_participants', 'min_participants',
            'preferred_mood', 'usage_requirements', 'version', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConversationFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationFeedback
        fields = [
            'id', 'conversation', 'user', 'accuracy_rating',
            'humor_rating', 'personality_rating', 'overall_rating',
            'what_worked', 'what_didnt_work', 'suggestions',
            'feedback_categories', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
