from rest_framework import serializers
from .models import Device, DeviceType, PersonalityTrait, DeviceRelationship


class PersonalityTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalityTrait
        fields = ['id', 'name', 'description', 'category', 'speech_patterns']
        read_only_fields = ['id']


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ['id', 'name', 'default_personality', 'icon', 'platform_category']
        read_only_fields = ['id']


class DeviceListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    device_type_name = serializers.CharField(source='device_type.name', read_only=True)
    
    class Meta:
        model = Device
        fields = [
            'id', 'name', 'device_type', 'device_type_name',
            'platform', 'personality_type', 'is_active', 'is_primary',
            'last_sync', 'last_usage', 'battery_level', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'device_type_name']


class DeviceSerializer(serializers.ModelSerializer):
    """Full serializer with all details"""
    personality_traits = PersonalityTraitSerializer(many=True, read_only=True)
    personality_trait_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=PersonalityTrait.objects.all(),
        source='personality_traits',
        write_only=True,
        required=False
    )
    device_type_details = DeviceTypeSerializer(source='device_type', read_only=True)
    total_apps = serializers.IntegerField(read_only=True)
    personality_description = serializers.CharField(read_only=True)
    
    class Meta:
        model = Device
        fields = [
            'id', 'name', 'device_type', 'device_type_details',
            'platform', 'device_identifier', 'model_name', 'os_version',
            'personality_type', 'personality_traits', 'personality_trait_ids',
            'custom_personality_notes', 'is_active', 'is_primary',
            'data_collection_enabled', 'last_sync', 'last_usage',
            'battery_level', 'created_at', 'updated_at',
            'personality_description', 'total_apps'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'personality_description', 'total_apps']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class DeviceRelationshipSerializer(serializers.ModelSerializer):
    device_a_details = DeviceListSerializer(source='device_a', read_only=True)
    device_b_details = DeviceListSerializer(source='device_b', read_only=True)
    
    class Meta:
        model = DeviceRelationship
        fields = [
            'id', 'device_a', 'device_a_details', 'device_b', 'device_b_details',
            'relationship_type', 'intensity', 'notes', 'interactions_count',
            'last_interaction', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        device_a = attrs.get('device_a')
        device_b = attrs.get('device_b')
        
        # Check if both devices belong to the same user
        user = self.context['request'].user
        if device_a.user != user or device_b.user != user:
            raise serializers.ValidationError("Both devices must belong to you")
        
        # Check if trying to create relationship with same device
        if device_a == device_b:
            raise serializers.ValidationError("A device cannot have a relationship with itself")
        
        return attrs
