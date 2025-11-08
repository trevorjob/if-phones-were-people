from rest_framework import serializers
from .models import UserStats, TrendAnalysis


class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStats
        fields = [
            'id', 'user', 'date', 'total_screen_time_all_devices',
            'total_pickups_all_devices', 'social_media_time',
            'productivity_time', 'entertainment_time', 'communication_time',
            'screen_time_rank', 'productivity_rank', 'weekly_trend',
            'notable_patterns', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class TrendAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendAnalysis
        fields = [
            'id', 'user', 'period_type', 'start_date', 'end_date',
            'screen_time_trend', 'app_usage_trends', 'category_trends',
            'key_insights', 'recommendations', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
