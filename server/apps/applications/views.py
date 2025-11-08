from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import App, AppCategory, DeviceApp, AppRelationship, AppPersonalityPreset
from .serializers import (
    AppSerializer, AppCategorySerializer, DeviceAppSerializer,
    DeviceAppListSerializer, AppRelationshipSerializer, AppPersonalityPresetSerializer
)


class AppViewSet(viewsets.ModelViewSet):
    """
    ViewSet for app registry
    """
    queryset = App.objects.all().select_related('category')
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'category', 'default_personality', 'is_social_media',
        'is_productivity', 'is_entertainment', 'is_work_related', 'is_game'
    ]
    search_fields = ['name', 'bundle_id']
    ordering_fields = ['name', 'addictive_potential', 'productivity_score']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular apps"""
        apps = self.get_queryset().order_by('-device_apps__count')[:20]
        serializer = self.get_serializer(apps, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def find_or_create(self, request):
        """Find app by bundle ID or create new one"""
        bundle_id = request.data.get('bundle_id')
        
        if not bundle_id:
            return Response(
                {"error": "bundle_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        app, created = App.objects.get_or_create(
            bundle_id=bundle_id,
            defaults=request.data
        )
        
        serializer = self.get_serializer(app)
        return Response(
            {
                "app": serializer.data,
                "created": created
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class AppCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for app categories
    """
    queryset = AppCategory.objects.all()
    serializer_class = AppCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class DeviceAppViewSet(viewsets.ModelViewSet):
    """
    ViewSet for device apps (apps installed on specific devices)
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'device', 'app', 'personality_override', 'is_active',
        'is_favorite', 'is_hidden', 'conversation_participation'
    ]
    search_fields = ['custom_name', 'app__name']
    ordering_fields = ['last_used', 'created_at']
    ordering = ['-is_favorite', '-last_used']
    
    def get_queryset(self):
        user = self.request.user
        return DeviceApp.objects.filter(
            device__user=user
        ).select_related('device', 'app', 'app__category')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DeviceAppListSerializer
        return DeviceAppSerializer
    
    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        """Toggle favorite status"""
        device_app = self.get_object()
        device_app.is_favorite = not device_app.is_favorite
        device_app.save()
        
        serializer = self.get_serializer(device_app)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_hidden(self, request, pk=None):
        """Toggle hidden status"""
        device_app = self.get_object()
        device_app.is_hidden = not device_app.is_hidden
        device_app.save()
        
        serializer = self.get_serializer(device_app)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def favorites(self, request):
        """Get only favorite apps"""
        apps = self.get_queryset().filter(is_favorite=True, is_active=True)
        serializer = self.get_serializer(apps, many=True)
        return Response(serializer.data)


class AppRelationshipViewSet(viewsets.ModelViewSet):
    """
    ViewSet for app relationships
    """
    serializer_class = AppRelationshipSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['relationship_type', 'same_device', 'app_a', 'app_b']
    
    def get_queryset(self):
        user = self.request.user
        return AppRelationship.objects.filter(
            app_a__device__user=user
        ).select_related('app_a', 'app_b', 'app_a__app', 'app_b__app')


class AppPersonalityPresetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for app personality presets (read-only)
    """
    queryset = AppPersonalityPreset.objects.all().prefetch_related('suitable_for_categories')
    serializer_class = AppPersonalityPresetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
