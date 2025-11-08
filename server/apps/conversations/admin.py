from django.contrib import admin
from .models import ConversationTrigger, Conversation, DeviceJournal, AppJournal, ConversationFeedback


@admin.register(ConversationTrigger)
class ConversationTriggerAdmin(admin.ModelAdmin):
    list_display = ['trigger_type', 'condition', 'is_active', 'created_at']
    list_filter = ['trigger_type', 'is_active', 'created_at']
    search_fields = ['description']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'conversation_type', 'mood', 'is_read', 'is_favorite', 'rating', 'created_at']
    list_filter = ['conversation_type', 'mood', 'is_read', 'is_favorite', 'is_ai_generated', 'created_at']
    search_fields = ['user__username', 'content']
    readonly_fields = ['created_at', 'model_used', 'tokens_used', 'generation_cost']
    filter_horizontal = ['participating_devices', 'participating_apps', 'triggers']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'conversation_type', 'mood', 'content')
        }),
        ('Participants', {
            'fields': ('participating_devices', 'participating_apps', 'triggers')
        }),
        ('Status', {
            'fields': ('is_read', 'is_favorite', 'rating')
        }),
        ('AI Generation', {
            'fields': ('is_ai_generated', 'model_used', 'generation_prompt', 'tokens_used', 'generation_cost'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(DeviceJournal)
class DeviceJournalAdmin(admin.ModelAdmin):
    list_display = ['device', 'date', 'mood', 'is_ai_generated', 'created_at']
    list_filter = ['mood', 'is_ai_generated', 'date', 'created_at']
    search_fields = ['device__name', 'content']
    readonly_fields = ['created_at', 'model_used']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('device', 'date', 'mood', 'content')
        }),
        ('AI Generation', {
            'fields': ('is_ai_generated', 'model_used', 'generation_prompt'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(AppJournal)
class AppJournalAdmin(admin.ModelAdmin):
    list_display = ['device_app', 'date', 'mood', 'is_ai_generated', 'created_at']
    list_filter = ['mood', 'is_ai_generated', 'date', 'created_at']
    search_fields = ['device_app__app__name', 'content']
    readonly_fields = ['created_at', 'model_used']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('device_app', 'date', 'mood', 'content')
        }),
        ('AI Generation', {
            'fields': ('is_ai_generated', 'model_used', 'generation_prompt'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ConversationFeedback)
class ConversationFeedbackAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'rating', 'feedback_type', 'created_at']
    list_filter = ['rating', 'feedback_type', 'created_at']
    search_fields = ['conversation__id', 'comment']
    readonly_fields = ['created_at']

