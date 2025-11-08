from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Conversation, ConversationTrigger, DeviceJournal, AppJournal,
    ConversationTemplate, ConversationFeedback
)
from .serializers import (
    ConversationSerializer, ConversationListSerializer,
    ConversationTriggerSerializer, DeviceJournalSerializer,
    AppJournalSerializer, ConversationTemplateSerializer,
    ConversationFeedbackSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for conversations
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conversation_type', 'mood', 'date', 'is_favorite', 'is_hidden', 'generation_status']
    ordering_fields = ['date', 'created_at', 'user_rating']
    ordering = ['-date', '-created_at']
    
    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(user=user).prefetch_related(
            'participating_devices', 'participating_apps', 'triggers'
        )
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer
    
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        """Rate a conversation"""
        conversation = self.get_object()
        rating = request.data.get('rating')
        
        if not rating or not (1 <= int(rating) <= 5):
            return Response(
                {"error": "Rating must be between 1 and 5"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversation.user_rating = rating
        conversation.user_feedback = request.data.get('feedback', '')
        conversation.save()
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        """Toggle favorite status"""
        conversation = self.get_object()
        conversation.is_favorite = not conversation.is_favorite
        conversation.save()
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_hidden(self, request, pk=None):
        """Toggle hidden status"""
        conversation = self.get_object()
        conversation.is_hidden = not conversation.is_hidden
        conversation.save()
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def favorites(self, request):
        """Get only favorite conversations"""
        conversations = self.get_queryset().filter(is_favorite=True, is_hidden=False)
        serializer = self.get_serializer(conversations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent conversations"""
        limit = int(request.query_params.get('limit', 10))
        conversations = self.get_queryset().filter(
            is_hidden=False,
            generation_status='completed'
        )[:limit]
        serializer = self.get_serializer(conversations, many=True)
        return Response(serializer.data)


class ConversationTriggerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for conversation triggers (admin-focused)
    """
    queryset = ConversationTrigger.objects.all()
    serializer_class = ConversationTriggerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['trigger_type', 'is_active']


class DeviceJournalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for device journals
    """
    serializer_class = DeviceJournalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['device', 'date', 'mood']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        user = self.request.user
        return DeviceJournal.objects.filter(
            device__user=user
        ).select_related('device').prefetch_related('mentioned_apps', 'mentioned_devices')
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent journal entries"""
        limit = int(request.query_params.get('limit', 10))
        journals = self.get_queryset()[:limit]
        serializer = self.get_serializer(journals, many=True)
        return Response(serializer.data)


class AppJournalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for app journals
    """
    serializer_class = AppJournalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['device_app', 'date', 'mood']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        user = self.request.user
        return AppJournal.objects.filter(
            device_app__device__user=user
        ).select_related('device_app', 'device_app__app').prefetch_related('mentioned_apps')
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent journal entries"""
        limit = int(request.query_params.get('limit', 10))
        journals = self.get_queryset()[:limit]
        serializer = self.get_serializer(journals, many=True)
        return Response(serializer.data)


class ConversationTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for conversation templates (admin-focused)
    """
    queryset = ConversationTemplate.objects.all()
    serializer_class = ConversationTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation_type', 'is_active']


class ConversationFeedbackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for conversation feedback
    """
    serializer_class = ConversationFeedbackSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conversation', 'overall_rating']
    ordering_fields = ['created_at', 'overall_rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        return ConversationFeedback.objects.filter(user=user).select_related('conversation')
