from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Device, DeviceType, PersonalityTrait, DeviceRelationship
from .serializers import (
    DeviceSerializer, DeviceListSerializer, DeviceTypeSerializer,
    PersonalityTraitSerializer, DeviceRelationshipSerializer
)


class DeviceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for device management
    
    list: Get all user's devices
    create: Add new device
    retrieve: Get device details
    update: Update device
    destroy: Delete device
    set_primary: Set device as primary
    sync: Update device sync status
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['platform', 'personality_type', 'is_active', 'is_primary', 'device_type']
    search_fields = ['name', 'model_name']
    ordering_fields = ['created_at', 'last_usage', 'name']
    ordering = ['-is_primary', '-last_usage']
    
    def get_queryset(self):
        return Device.objects.filter(user=self.request.user).select_related(
            'device_type'
        ).prefetch_related('personality_traits')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DeviceListSerializer
        return DeviceSerializer
    
    @action(detail=True, methods=['post'])
    def set_primary(self, request, pk=None):
        """Set this device as the primary device"""
        device = self.get_object()
        
        # Remove primary status from all other devices
        Device.objects.filter(user=request.user, is_primary=True).update(is_primary=False)
        
        # Set this device as primary
        device.is_primary = True
        device.save()
        
        serializer = self.get_serializer(device)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def sync(self, request, pk=None):
        """Update device sync status and metadata"""
        device = self.get_object()
        
        device.last_sync = timezone.now()
        
        # Update battery level if provided
        if 'battery_level' in request.data:
            device.battery_level = request.data['battery_level']
        
        # Update last usage if provided
        if 'last_usage' in request.data:
            device.last_usage = request.data['last_usage']
        
        device.save()
        
        serializer = self.get_serializer(device)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active devices"""
        devices = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(devices, many=True)
        return Response(serializer.data)


class DeviceTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for device types (read-only)
    """
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'platform_category']


class PersonalityTraitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for personality traits (read-only)
    """
    queryset = PersonalityTrait.objects.all()
    serializer_class = PersonalityTraitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']


class DeviceRelationshipViewSet(viewsets.ModelViewSet):
    """
    ViewSet for device relationships
    """
    serializer_class = DeviceRelationshipSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['relationship_type', 'device_a', 'device_b']
    
    def get_queryset(self):
        user = self.request.user
        return DeviceRelationship.objects.filter(
            device_a__user=user
        ).select_related('device_a', 'device_b')
    
    @action(detail=True, methods=['post'])
    def increment_interaction(self, request, pk=None):
        """Increment the interaction count for this relationship"""
        relationship = self.get_object()
        relationship.interactions_count += 1
        relationship.last_interaction = timezone.now()
        relationship.save()
        
        serializer = self.get_serializer(relationship)
        return Response(serializer.data)
