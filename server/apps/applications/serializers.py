from rest_framework import serializers
from .models import App, AppCategory, DeviceApp, AppRelationship, AppPersonalityPreset


class AppCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppCategory
        fields = ['id', 'name', 'description', 'icon', 'color', 'default_personality_traits']
        read_only_fields = ['id']


class AppSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    total_users = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = App
        fields = [
            'id', 'name', 'bundle_id', 'category', 'category_name',
            'ios_bundle_id', 'android_package', 'windows_exe', 'mac_bundle_id',
            'icon_url', 'primary_color', 'default_personality',
            'personality_description', 'is_social_media', 'is_productivity',
            'is_entertainment', 'is_work_related', 'is_game',
            'typical_session_length', 'addictive_potential', 'productivity_score',
            'total_users', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_users']


class DeviceAppListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    app_name = serializers.CharField(source='app.name', read_only=True)
    app_category = serializers.CharField(source='app.category.name', read_only=True)
    display_name = serializers.CharField(read_only=True)
    effective_personality = serializers.CharField(read_only=True)
    
    class Meta:
        model = DeviceApp
        fields = [
            'id', 'device', 'app', 'app_name', 'app_category',
            'custom_name', 'display_name', 'personality_override',
            'effective_personality', 'is_active', 'is_favorite',
            'last_used', 'conversation_participation', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'display_name', 'effective_personality']


class DeviceAppSerializer(serializers.ModelSerializer):
    """Full serializer with all details"""
    app_details = AppSerializer(source='app', read_only=True)
    display_name = serializers.CharField(read_only=True)
    effective_personality = serializers.CharField(read_only=True)
    personality_description = serializers.CharField(read_only=True)
    
    class Meta:
        model = DeviceApp
        fields = [
            'id', 'device', 'app', 'app_details', 'custom_name', 'display_name',
            'personality_override', 'effective_personality', 'custom_personality_notes',
            'personality_description', 'is_active', 'is_favorite', 'is_hidden',
            'first_installed', 'last_used', 'version', 'conversation_participation',
            'conversation_frequency', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'first_installed', 'created_at', 'updated_at', 
                            'display_name', 'effective_personality', 'personality_description']
    
    def validate(self, attrs):
        device = attrs.get('device')
        user = self.context['request'].user
        
        # Check if device belongs to user
        if device.user != user:
            raise serializers.ValidationError("This device does not belong to you")
        
        return attrs


class AppRelationshipSerializer(serializers.ModelSerializer):
    app_a_details = DeviceAppListSerializer(source='app_a', read_only=True)
    app_b_details = DeviceAppListSerializer(source='app_b', read_only=True)
    
    class Meta:
        model = AppRelationship
        fields = [
            'id', 'app_a', 'app_a_details', 'app_b', 'app_b_details',
            'relationship_type', 'same_device', 'user_created',
            'interactions_count', 'co_usage_frequency', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        app_a = attrs.get('app_a')
        app_b = attrs.get('app_b')
        user = self.context['request'].user
        
        # Check if both apps belong to user's devices
        if app_a.device.user != user or app_b.device.user != user:
            raise serializers.ValidationError("Both apps must belong to your devices")
        
        # Check if trying to create relationship with same app
        if app_a == app_b:
            raise serializers.ValidationError("An app cannot have a relationship with itself")
        
        # Auto-set same_device flag
        attrs['same_device'] = (app_a.device == app_b.device)
        
        return attrs


class AppPersonalityPresetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPersonalityPreset
        fields = [
            'id', 'name', 'description', 'speech_patterns',
            'conversation_style', 'common_phrases', 'reaction_triggers'
        ]
        read_only_fields = ['id']
