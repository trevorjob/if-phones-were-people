"""
AI Service for generating conversations, journals, and insights using OpenAI
"""
import openai
from django.conf import settings
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('ai_engine')

# Set OpenAI API key
openai.api_key = settings.OPENAI_API_KEY


class AIGenerationService:
    """Service for AI content generation"""
    
    DEFAULT_MODEL = "gpt-4"
    DEFAULT_TEMPERATURE = 0.8
    DEFAULT_MAX_TOKENS = 1000
    
    @staticmethod
    def generate_conversation(
        devices: List,
        apps: List,
        usage_data: Dict,
        conversation_type: str = 'daily_recap',
        mood: str = 'humorous',
        triggers: Optional[List] = None
    ) -> Dict:
        """
        Generate a conversation between devices and apps
        
        Args:
            devices: List of Device objects
            apps: List of DeviceApp objects  
            usage_data: Dictionary with usage statistics
            conversation_type: Type of conversation
            mood: Desired mood/tone
            triggers: List of ConversationTrigger objects
            
        Returns:
            Dictionary with conversation content and metadata
        """
        try:
            # Build system prompt
            system_prompt = AIGenerationService._build_conversation_system_prompt(
                conversation_type, mood
            )
            
            # Build user prompt with context
            user_prompt = AIGenerationService._build_conversation_user_prompt(
                devices, apps, usage_data, triggers
            )
            
            # Call OpenAI
            response = openai.ChatCompletion.create(
                model=AIGenerationService.DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=AIGenerationService.DEFAULT_TEMPERATURE,
                max_tokens=AIGenerationService.DEFAULT_MAX_TOKENS
            )
            
            conversation_content = response.choices[0].message.content
            
            # Calculate cost (approximate)
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            
            # GPT-4 pricing (as of 2024): $0.03 per 1K prompt tokens, $0.06 per 1K completion tokens
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000
            
            logger.info(f"Generated conversation: {total_tokens} tokens, ${cost:.4f}")
            
            return {
                'content': conversation_content,
                'model_used': response.model,
                'generation_prompt': user_prompt,
                'tokens_used': total_tokens,
                'cost': cost,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error generating conversation: {str(e)}")
            return {
                'content': '',
                'error': str(e),
                'success': False
            }
    
    @staticmethod
    def _build_conversation_system_prompt(conversation_type: str, mood: str) -> str:
        """Build the system prompt for conversation generation"""
        
        base_prompt = """You are a creative AI that generates entertaining conversations between personified devices and apps.

Rules:
1. Each device and app has a distinct personality - stay consistent with their character
2. Reference actual usage data naturally in dialogue
3. Make it funny but insightful
4. Format as a script with character names
5. Keep it under 500 words
6. Use the specified mood and conversation type

Character Format Example:
iPhone: *sighs* So, we need to talk about yesterday...
Instagram: OMG what happened?!
"""
        
        conversation_types = {
            'daily_recap': 'Create a daily recap where devices discuss the day\'s usage',
            'usage_intervention': 'Devices express concern about excessive usage',
            'pattern_discussion': 'Discuss detected usage patterns',
            'goal_check_in': 'Check in on user\'s digital wellness goals',
            'app_drama': 'Apps argue about screen time and attention',
            'device_gossip': 'Devices gossip about the user\'s habits',
            'productivity_roast': 'Devices roast the user about procrastination',
            'social_comparison': 'Compare usage with friends',
            'milestone_celebration': 'Celebrate an achievement or milestone',
            'friend_visit': 'A friend\'s device visits and interacts',
            'emergency_meeting': 'Urgent meeting about concerning behavior'
        }
        
        mood_descriptions = {
            'humorous': 'Keep it light and funny',
            'supportive': 'Be encouraging and positive',
            'dramatic': 'Amp up the drama and exaggeration',
            'sarcastic': 'Use witty sarcasm and dry humor',
            'educational': 'Focus on insights and learning',
            'gossipy': 'Make it juicy and gossipy',
            'competitive': 'Turn it into a competition',
            'concerned': 'Express genuine concern',
            'celebratory': 'Celebrate successes',
            'chaotic': 'Make it wild and unpredictable'
        }
        
        conversation_context = conversation_types.get(conversation_type, 'Have a general conversation')
        mood_context = mood_descriptions.get(mood, 'Be entertaining')
        
        return f"{base_prompt}\n\nConversation Type: {conversation_context}\nMood: {mood_context}"
    
    @staticmethod
    def _build_conversation_user_prompt(
        devices: List,
        apps: List,
        usage_data: Dict,
        triggers: Optional[List] = None
    ) -> str:
        """Build the user prompt with all context"""
        
        prompt_parts = []
        
        # Participants
        prompt_parts.append("=== PARTICIPANTS ===")
        for device in devices:
            prompt_parts.append(
                f"\n{device.name} ({device.platform}):"
                f"\n- Personality: {device.personality_type}"
                f"\n- Description: {device.personality_description}"
            )
        
        for app in apps:
            prompt_parts.append(
                f"\n{app.display_name}:"
                f"\n- Personality: {app.effective_personality}"
                f"\n- Type: {app.app.category.name if app.app.category else 'Unknown'}"
            )
        
        # Usage Context
        prompt_parts.append("\n\n=== USAGE DATA ===")
        if usage_data.get('total_screen_time'):
            hours = usage_data['total_screen_time'] / 60
            prompt_parts.append(f"Total Screen Time: {hours:.1f} hours")
        
        if usage_data.get('top_apps'):
            prompt_parts.append(f"Most Used Apps: {', '.join(usage_data['top_apps'])}")
        
        if usage_data.get('unlock_count'):
            prompt_parts.append(f"Phone Unlocks: {usage_data['unlock_count']} times")
        
        if usage_data.get('patterns'):
            prompt_parts.append(f"Detected Patterns: {', '.join(usage_data['patterns'])}")
        
        # Triggers
        if triggers:
            prompt_parts.append("\n\n=== TRIGGERS ===")
            for trigger in triggers:
                prompt_parts.append(f"- {trigger.description}")
        
        # Additional context
        if usage_data.get('notes'):
            prompt_parts.append(f"\n\nAdditional Context: {usage_data['notes']}")
        
        prompt_parts.append("\n\nGenerate the conversation now:")
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def generate_device_journal(
        device,
        date,
        usage_summary: Dict,
        notable_events: List[str],
        mentioned_apps: List = None
    ) -> Dict:
        """
        Generate a journal entry from a device's perspective
        
        Args:
            device: Device object
            date: Date of journal entry
            usage_summary: Summary of usage for the day
            notable_events: List of notable events
            mentioned_apps: Apps to mention in journal
            
        Returns:
            Dictionary with journal content and metadata
        """
        try:
            system_prompt = f"""You are {device.name}, a {device.platform} device with a {device.personality_type} personality.
            
Your personality: {device.personality_description}

Write a personal journal entry about today from your perspective as a device. Be introspective and stay in character.
Keep it under 300 words. Write in first person."""
            
            # Build context
            context_parts = [f"Date: {date}"]
            
            if usage_summary.get('screen_time'):
                hours = usage_summary['screen_time'] / 60
                context_parts.append(f"I was used for {hours:.1f} hours today")
            
            if usage_summary.get('unlocks'):
                context_parts.append(f"Unlocked {usage_summary['unlocks']} times")
            
            if notable_events:
                context_parts.append(f"Notable events: {', '.join(notable_events)}")
            
            if mentioned_apps:
                app_names = [app.display_name for app in mentioned_apps]
                context_parts.append(f"Active apps: {', '.join(app_names)}")
            
            user_prompt = "\n".join(context_parts) + "\n\nWrite your journal entry:"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use cheaper model for journals
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=400
            )
            
            content = response.choices[0].message.content
            
            logger.info(f"Generated device journal for {device.name}")
            
            return {
                'content': content,
                'model_used': response.model,
                'generation_prompt': user_prompt,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error generating device journal: {str(e)}")
            return {
                'content': '',
                'error': str(e),
                'success': False
            }
    
    @staticmethod
    def generate_app_journal(
        device_app,
        date,
        usage_stats: Dict,
        session_highlights: List[str]
    ) -> Dict:
        """
        Generate a journal entry from an app's perspective
        
        Args:
            device_app: DeviceApp object
            date: Date of journal entry
            usage_stats: Usage statistics for the day
            session_highlights: Highlights from usage sessions
            
        Returns:
            Dictionary with journal content and metadata
        """
        try:
            system_prompt = f"""You are {device_app.display_name}, an app with a {device_app.effective_personality} personality.

Write a brief journal entry (150 words max) about today from your perspective. Stay in character and be entertaining."""
            
            context_parts = [f"Date: {date}"]
            
            if usage_stats.get('time_spent'):
                minutes = usage_stats['time_spent']
                context_parts.append(f"User spent {minutes} minutes with me")
            
            if usage_stats.get('launch_count'):
                context_parts.append(f"Opened {usage_stats['launch_count']} times")
            
            if session_highlights:
                context_parts.append(f"Highlights: {', '.join(session_highlights)}")
            
            user_prompt = "\n".join(context_parts) + "\n\nWrite your journal entry:"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=250
            )
            
            content = response.choices[0].message.content
            
            logger.info(f"Generated app journal for {device_app.display_name}")
            
            return {
                'content': content,
                'model_used': response.model,
                'generation_prompt': user_prompt,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error generating app journal: {str(e)}")
            return {
                'content': '',
                'error': str(e),
                'success': False
            }
