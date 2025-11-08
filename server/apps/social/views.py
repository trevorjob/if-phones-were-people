from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import FriendConnection, TemporaryDeviceConnection, Challenge
from .serializers import (
    FriendConnectionSerializer, TemporaryDeviceConnectionSerializer,
    ChallengeSerializer
)


class FriendConnectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for friend connections
    """
    serializer_class = FriendConnectionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'can_compare_stats']
    
    def get_queryset(self):
        user = self.request.user
        return FriendConnection.objects.filter(user=user).select_related('friend_user')
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active friend connections"""
        friends = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(friends, many=True)
        return Response(serializer.data)


class TemporaryDeviceConnectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for temporary device connections
    """
    serializer_class = TemporaryDeviceConnectionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'host_user', 'visitor_user']
    
    def get_queryset(self):
        user = self.request.user
        return TemporaryDeviceConnection.objects.filter(
            host_user=user
        ).select_related('host_user', 'visitor_user', 'visitor_device')
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active connections"""
        connections = self.get_queryset().filter(is_active=True)
        # Filter out expired ones
        active_connections = [c for c in connections if not c.is_expired()]
        serializer = self.get_serializer(active_connections, many=True)
        return Response(serializer.data)


class ChallengeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for challenges
    """
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['challenge_type', 'is_active']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-start_date']
    
    def get_queryset(self):
        user = self.request.user
        return Challenge.objects.filter(
            participants=user
        ).select_related('creator', 'winner').prefetch_related('participants')
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active challenges"""
        challenges = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(challenges, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a challenge"""
        challenge = self.get_object()
        challenge.participants.add(request.user)
        serializer = self.get_serializer(challenge)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a challenge"""
        challenge = self.get_object()
        challenge.participants.remove(request.user)
        serializer = self.get_serializer(challenge)
        return Response(serializer.data)
