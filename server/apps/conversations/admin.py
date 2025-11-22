from django.contrib import admin
from .models import ConversationTrigger, Conversation, DeviceJournal, AppJournal, ConversationFeedback


@admin.register(ConversationTrigger)
class ConversationTriggerAdmin(admin.ModelAdmin):
    list_display = ['name', 'trigger_type', 'priority', 'is_active']
    list_filter = ['trigger_type', 'is_active']
    search_fields = ['name', 'description']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'conversation_type', 'mood', 'is_favorite', 'user_rating', 'generation_status', 'created_at']
    list_filter = ['conversation_type', 'mood', 'is_favorite', 'generation_status', 'date']
    search_fields = ['user__username', 'content', 'summary']
    readonly_fields = ['id', 'created_at', 'updated_at', 'ai_model_used', 'generation_tokens', 'generation_cost']
    filter_horizontal = ['participating_devices', 'participating_apps', 'triggers']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'date', 'conversation_type', 'mood', 'content', 'summary')
        }),
        ('Participants', {
            'fields': ('participating_devices', 'participating_apps', 'triggers')
        }),
        ('User Interaction', {
            'fields': ('is_favorite', 'is_hidden', 'user_rating', 'user_feedback')
        }),
        ('AI Generation', {
            'fields': ('generation_status', 'ai_model_used', 'generation_prompt', 'generation_tokens', 'generation_cost', 'trigger_data'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DeviceJournal)
class DeviceJournalAdmin(admin.ModelAdmin):
    list_display = ['device', 'date', 'mood', 'ai_generated', 'created_at']
    list_filter = ['mood', 'ai_generated', 'date']
    search_fields = ['device__name', 'content', 'insights']
    readonly_fields = ['id', 'created_at', 'updated_at']
    filter_horizontal = ['mentioned_apps', 'mentioned_devices']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('device', 'date', 'mood', 'content', 'insights')
        }),
        ('Events & Context', {
            'fields': ('notable_events', 'usage_summary', 'personality_development')
        }),
        ('Relationships', {
            'fields': ('mentioned_apps', 'mentioned_devices')
        }),
        ('AI Generation', {
            'fields': ('ai_generated', 'generation_prompt'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AppJournal)
class AppJournalAdmin(admin.ModelAdmin):
    list_display = ['device_app', 'date', 'mood', 'ai_generated', 'usage_satisfaction', 'created_at']
    list_filter = ['mood', 'ai_generated', 'date']
    search_fields = ['device_app__app__name', 'device_app__custom_name', 'content', 'user_behavior_notes']
    readonly_fields = ['id', 'created_at', 'updated_at']
    filter_horizontal = ['mentioned_apps']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('device_app', 'date', 'mood', 'content', 'user_behavior_notes')
        }),
        ('Experience & Reflection', {
            'fields': ('session_highlights', 'app_interactions', 'usage_satisfaction', 'productivity_contribution')
        }),
        ('Relationships', {
            'fields': ('mentioned_apps',)
        }),
        ('AI Generation', {
            'fields': ('ai_generated', 'generation_prompt'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ConversationFeedback)
class ConversationFeedbackAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'user', 'overall_rating', 'accuracy_rating', 'humor_rating', 'created_at']
    list_filter = ['overall_rating', 'accuracy_rating', 'humor_rating', 'personality_rating']
    search_fields = ['conversation__id', 'what_worked', 'what_didnt_work', 'suggestions']
    readonly_fields = ['created_at']

