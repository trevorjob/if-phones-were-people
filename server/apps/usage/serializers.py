from rest_framework import serializers
from .models import UsageData, AppUsage, UsagePattern, UsageGoal
from apps.applications.serializers import DeviceAppListSerializer


class UsageDataSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)
    screen_time_hours = serializers.FloatField(read_only=True)
    usage_intensity = serializers.CharField(read_only=True)
    
    class Meta:
        model = UsageData
        fields = [
            'id', 'device', 'device_name', 'date', 'total_screen_time',
            'screen_time_hours', 'unlock_count', 'pickup_count',
            'notification_count', 'first_pickup_time', 'last_usage_time',
            'longest_session_minutes', 'average_session_minutes',
            'hourly_usage', 'battery_start', 'battery_end',
            'charging_time_minutes', 'weekday', 'is_weekend', 'is_holiday',
            'data_completeness', 'collection_method', 'usage_intensity',
            'synced_at', 'updated_at'
        ]
        read_only_fields = ['id', 'synced_at', 'updated_at', 'screen_time_hours', 'usage_intensity']
    
    def validate(self, attrs):
        device = attrs.get('device')
        user = self.context['request'].user
        
        # Check if device belongs to user
        if device.user != user:
            raise serializers.ValidationError("This device does not belong to you")
        
        return attrs


class AppUsageSerializer(serializers.ModelSerializer):
    app_name = serializers.CharField(source='device_app.display_name', read_only=True)
    device_app_details = DeviceAppListSerializer(source='device_app', read_only=True)
    time_spent_hours = serializers.FloatField(read_only=True)
    usage_intensity = serializers.CharField(read_only=True)
    
    class Meta:
        model = AppUsage
        fields = [
            'id', 'device_app', 'device_app_details', 'app_name', 'date',
            'time_spent_minutes', 'time_spent_hours', 'launch_count',
            'notification_count', 'background_time_minutes', 'session_count',
            'longest_session_minutes', 'average_session_minutes',
            'first_launch_time', 'last_usage_time', 'peak_usage_hour',
            'hourly_usage', 'scrolled_distance', 'items_viewed',
            'actions_performed', 'usage_context', 'data_completeness',
            'estimated', 'usage_intensity', 'synced_at', 'updated_at'
        ]
        read_only_fields = ['id', 'synced_at', 'updated_at', 'time_spent_hours', 'usage_intensity']
    
    def validate(self, attrs):
        device_app = attrs.get('device_app')
        user = self.context['request'].user
        
        # Check if device app belongs to user
        if device_app.device.user != user:
            raise serializers.ValidationError("This app does not belong to your devices")
        
        return attrs


class UsagePatternSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True, allow_null=True)
    apps_involved_details = DeviceAppListSerializer(source='apps_involved', many=True, read_only=True)
    
    class Meta:
        model = UsagePattern
        fields = [
            'id', 'user', 'device', 'device_name', 'pattern_type',
            'description', 'confidence_score', 'start_date', 'end_date',
            'days_observed', 'pattern_data', 'apps_involved',
            'apps_involved_details', 'frequency', 'strength',
            'impact_on_productivity', 'impact_on_wellness', 'is_active',
            'user_acknowledged', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UsageGoalSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True, allow_null=True)
    app_name = serializers.CharField(source='app.display_name', read_only=True, allow_null=True)
    
    class Meta:
        model = UsageGoal
        fields = [
            'id', 'user', 'device', 'device_name', 'app', 'app_name',
            'goal_type', 'target_minutes_daily', 'target_sessions_daily',
            'cutoff_time', 'start_date', 'end_date', 'duration_days',
            'current_streak', 'best_streak', 'total_successful_days',
            'is_active', 'completion_percentage', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'current_streak', 'best_streak',
            'total_successful_days', 'completion_percentage',
            'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate(self, attrs):
        device = attrs.get('device')
        app = attrs.get('app')
        user = self.context['request'].user
        
        # Check ownership
        if device and device.user != user:
            raise serializers.ValidationError("This device does not belong to you")
        
        if app and app.device.user != user:
            raise serializers.ValidationError("This app does not belong to your devices")
        
        return attrs


class BulkUsageDataSerializer(serializers.Serializer):
    """Serializer for bulk upload of usage data"""
    device_id = serializers.UUIDField()
    date = serializers.DateField()
    total_screen_time = serializers.IntegerField()
    unlock_count = serializers.IntegerField(required=False, default=0)
    pickup_count = serializers.IntegerField(required=False, default=0)
    notification_count = serializers.IntegerField(required=False, default=0)
    first_pickup_time = serializers.TimeField(required=False, allow_null=True)
    last_usage_time = serializers.TimeField(required=False, allow_null=True)
    hourly_usage = serializers.ListField(required=False, default=list)
    battery_start = serializers.IntegerField(required=False, allow_null=True)
    battery_end = serializers.IntegerField(required=False, allow_null=True)
    collection_method = serializers.CharField(required=False, default='api_sync')
    
    def validate_device_id(self, value):
        from apps.devices.models import Device
        user = self.context['request'].user
        
        if not Device.objects.filter(id=value, user=user).exists():
            raise serializers.ValidationError("Device not found or does not belong to you")
        
        return value
