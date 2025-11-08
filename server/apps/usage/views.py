from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Avg
from datetime import date, timedelta
from .models import UsageData, AppUsage, UsagePattern, UsageGoal
from .serializers import (
    UsageDataSerializer, AppUsageSerializer, UsagePatternSerializer,
    UsageGoalSerializer, BulkUsageDataSerializer
)


class UsageDataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for device usage data
    """
    serializer_class = UsageDataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['device', 'date', 'is_weekend', 'collection_method']
    ordering_fields = ['date', 'total_screen_time']
    ordering = ['-date']
    
    def get_queryset(self):
        user = self.request.user
        return UsageData.objects.filter(
            device__user=user
        ).select_related('device')
    
    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        """Upload multiple days of usage data"""
        if not isinstance(request.data, list):
            return Response(
                {"error": "Expected a list of usage data"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = BulkUsageDataSerializer(
            data=request.data,
            many=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        created_count = 0
        updated_count = 0
        
        for item in serializer.validated_data:
            from apps.devices.models import Device
            device = Device.objects.get(id=item['device_id'])
            
            # Calculate weekday and weekend flag
            usage_date = item['date']
            weekday = usage_date.weekday()
            
            usage_data, created = UsageData.objects.update_or_create(
                device=device,
                date=usage_date,
                defaults={
                    'total_screen_time': item['total_screen_time'],
                    'unlock_count': item.get('unlock_count', 0),
                    'pickup_count': item.get('pickup_count', 0),
                    'notification_count': item.get('notification_count', 0),
                    'first_pickup_time': item.get('first_pickup_time'),
                    'last_usage_time': item.get('last_usage_time'),
                    'hourly_usage': item.get('hourly_usage', []),
                    'battery_start': item.get('battery_start'),
                    'battery_end': item.get('battery_end'),
                    'weekday': weekday,
                    'is_weekend': weekday >= 5,
                    'collection_method': item.get('collection_method', 'api_sync'),
                }
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1
        
        return Response({
            "message": f"Successfully processed {len(serializer.validated_data)} records",
            "created": created_count,
            "updated": updated_count
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get usage summary for a date range"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date', str(date.today()))
        device_id = request.query_params.get('device_id')
        
        if not start_date:
            # Default to last 7 days
            start_date = str(date.today() - timedelta(days=7))
        
        queryset = self.get_queryset().filter(
            date__gte=start_date,
            date__lte=end_date
        )
        
        if device_id:
            queryset = queryset.filter(device_id=device_id)
        
        summary = queryset.aggregate(
            total_screen_time=Sum('total_screen_time'),
            avg_screen_time=Avg('total_screen_time'),
            total_unlocks=Sum('unlock_count'),
            total_pickups=Sum('pickup_count'),
            total_notifications=Sum('notification_count')
        )
        
        return Response({
            'start_date': start_date,
            'end_date': end_date,
            'summary': summary,
            'days_count': queryset.count()
        })


class AppUsageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for app usage data
    """
    serializer_class = AppUsageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['device_app', 'date', 'estimated']
    ordering_fields = ['date', 'time_spent_minutes', 'launch_count']
    ordering = ['-date', '-time_spent_minutes']
    
    def get_queryset(self):
        user = self.request.user
        return AppUsage.objects.filter(
            device_app__device__user=user
        ).select_related('device_app', 'device_app__app', 'device_app__device')
    
    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        """Upload multiple app usage records"""
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def top_apps(self, request):
        """Get top apps by usage time"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date', str(date.today()))
        limit = int(request.query_params.get('limit', 10))
        
        if not start_date:
            start_date = str(date.today() - timedelta(days=7))
        
        queryset = self.get_queryset().filter(
            date__gte=start_date,
            date__lte=end_date
        )
        
        # Group by device_app and sum time spent
        from django.db.models import Sum
        top_apps = queryset.values(
            'device_app', 'device_app__display_name'
        ).annotate(
            total_time=Sum('time_spent_minutes')
        ).order_by('-total_time')[:limit]
        
        return Response(list(top_apps))


class UsagePatternViewSet(viewsets.ModelViewSet):
    """
    ViewSet for usage patterns
    """
    serializer_class = UsagePatternSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['pattern_type', 'device', 'frequency', 'strength', 'is_active', 'user_acknowledged']
    ordering_fields = ['created_at', 'start_date', 'confidence_score']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        return UsagePattern.objects.filter(user=user).prefetch_related('apps_involved')
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Mark pattern as acknowledged by user"""
        pattern = self.get_object()
        pattern.user_acknowledged = True
        pattern.save()
        
        serializer = self.get_serializer(pattern)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active patterns"""
        patterns = self.get_queryset().filter(is_active=True, end_date__isnull=True)
        serializer = self.get_serializer(patterns, many=True)
        return Response(serializer.data)


class UsageGoalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for usage goals
    """
    serializer_class = UsageGoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal_type', 'device', 'app', 'is_active']
    ordering_fields = ['created_at', 'start_date', 'completion_percentage']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        return UsageGoal.objects.filter(user=user).select_related('device', 'app')
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active goals"""
        goals = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(goals, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Update goal progress manually"""
        goal = self.get_object()
        
        # This would typically be called by a background task
        # For now, just increment success days if provided
        if request.data.get('success'):
            goal.total_successful_days += 1
            goal.current_streak += 1
            if goal.current_streak > goal.best_streak:
                goal.best_streak = goal.current_streak
        else:
            goal.current_streak = 0
        
        goal.save()
        
        serializer = self.get_serializer(goal)
        return Response(serializer.data)
