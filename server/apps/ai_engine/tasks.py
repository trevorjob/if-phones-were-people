"""
Celery tasks for AI engine
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django.db.models import Sum, Avg, Count, F, Q
from apps.ai_engine.services import AIGenerationService
from apps.conversations.models import Conversation, DeviceJournal, AppJournal
from apps.devices.models import Device
from apps.applications.models import DeviceApp
from apps.usage.models import UsageData, AppUsage
import logging

logger = logging.getLogger('ai_engine')


@shared_task(name='apps.ai_engine.tasks.generate_daily_conversations')
def generate_daily_conversations():
    """
    Generate daily conversations for all active users
    Runs at 6 AM daily
    """
    logger.info("Starting daily conversation generation")
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    yesterday = timezone.now().date() - timedelta(days=1)
    generated_count = 0
    error_count = 0
    
    # Get users who had activity yesterday
    active_users = User.objects.filter(
        devices__usage_data__date=yesterday
    ).distinct()
    
    for user in active_users:
        try:
            result = generate_conversation_for_user(user, yesterday)
            if result:
                generated_count += 1
            else:
                error_count += 1
        except Exception as e:
            logger.error(f"Error generating conversation for user {user.id}: {str(e)}")
            error_count += 1
    
    logger.info(f"Daily conversation generation complete: {generated_count} success, {error_count} errors")
    return {
        'success': generated_count,
        'errors': error_count,
        'date': str(yesterday)
    }


def generate_conversation_for_user(user, date):
    """Generate a conversation for a specific user and date"""
    try:
        # Get user's devices
        devices = list(user.devices.filter(is_active=True)[:3])  # Limit to 3 devices
        if not devices:
            logger.info(f"No active devices for user {user.id}")
            return False
        
        # Get most used apps from yesterday
        top_apps = AppUsage.objects.filter(
            device_app__device__user=user,
            date=date
        ).order_by('-time_spent_minutes')[:5]  # Top 5 apps
        
        device_apps = [au.device_app for au in top_apps if au.device_app]
        
        if not device_apps:
            logger.info(f"No app usage for user {user.id} on {date}")
            return False
        
        # Gather usage statistics
        total_usage = UsageData.objects.filter(
            device__user=user,
            date=date
        ).aggregate(
            total_time=Sum('total_screen_time'),
            total_unlocks=Sum('unlock_count')
        )
        
        usage_data = {
            'total_screen_time': total_usage['total_time'] or 0,
            'unlock_count': total_usage['total_unlocks'] or 0,
            'top_apps': [app.display_name for app in device_apps],
            'patterns': []
        }
        
        # Check for patterns
        from apps.usage.models import UsagePattern
        patterns = UsagePattern.objects.filter(
            user=user,
            start_date=date
        ).values_list('pattern_type', flat=True)
        usage_data['patterns'] = list(patterns)
        
        # Determine conversation type and mood
        conversation_type = 'daily_recap'
        mood = 'humorous'
        
        # Adjust based on usage
        if usage_data['total_screen_time'] > 360:  # More than 6 hours
            conversation_type = 'usage_intervention'
            mood = 'concerned'
        elif usage_data['patterns']:
            conversation_type = 'pattern_discussion'
        
        # Generate conversation using AI
        ai_result = AIGenerationService.generate_conversation(
            devices=devices,
            apps=device_apps,
            usage_data=usage_data,
            conversation_type=conversation_type,
            mood=mood
        )
        
        if ai_result['success']:
            # Save conversation
            with transaction.atomic():
                conversation = Conversation.objects.create(
                    user=user,
                    conversation_type=conversation_type,
                    mood=mood,
                    content=ai_result['content'],
                    ai_model_used=ai_result['model_used'],
                    generation_prompt=ai_result['generation_prompt'],
                    generation_tokens=ai_result['tokens_used'],
                    generation_cost=ai_result['cost'],
                    generation_status='completed'
                )
                
                # Link participants
                conversation.participating_devices.set(devices)
                conversation.participating_apps.set(device_apps)
                
                logger.info(f"Generated conversation {conversation.id} for user {user.id}")
                return True
        else:
            logger.error(f"AI generation failed for user {user.id}: {ai_result.get('error')}")
            return False
            
    except Exception as e:
        logger.error(f"Error in generate_conversation_for_user for user {user.id}: {str(e)}")
        return False


@shared_task(name='apps.ai_engine.tasks.generate_daily_journals')
def generate_daily_journals():
    """
    Generate device and app journals for previous day
    Runs at 11 PM daily
    """
    logger.info("Starting daily journal generation")
    
    today = timezone.now().date()
    generated_count = 0
    error_count = 0
    
    # Generate device journals
    devices = Device.objects.filter(
        is_active=True,
        usage_data__date=today
    ).distinct()
    
    for device in devices:
        try:
            result = generate_device_journal_entry(device, today)
            if result:
                generated_count += 1
            else:
                error_count += 1
        except Exception as e:
            logger.error(f"Error generating device journal for {device.id}: {str(e)}")
            error_count += 1
    
    # Generate app journals (for top apps only)
    # Query AppUsage directly since there's no direct link through DeviceApp
    top_app_usage = AppUsage.objects.filter(
        date=today
    ).values('device_app').annotate(
        total_time=Sum('time_spent_minutes')
    ).order_by('-total_time')[:50]
    
    device_app_ids = [item['device_app'] for item in top_app_usage]
    top_device_apps = DeviceApp.objects.filter(id__in=device_app_ids)
    
    for device_app in top_device_apps:
        try:
            result = generate_app_journal_entry(device_app, today)
            if result:
                generated_count += 1
            else:
                error_count += 1
        except Exception as e:
            logger.error(f"Error generating app journal for {device_app.id}: {str(e)}")
            error_count += 1
    
    logger.info(f"Daily journal generation complete: {generated_count} success, {error_count} errors")
    return {
        'success': generated_count,
        'errors': error_count,
        'date': str(today)
    }


def generate_device_journal_entry(device, date):
    """Generate a journal entry for a device"""
    try:
        # Get usage summary
        usage = UsageData.objects.filter(device=device, date=date).first()
        if not usage:
            return False
        
        usage_summary = {
            'screen_time': usage.total_screen_time,
            'unlocks': usage.unlock_count
        }
        
        # Notable events
        notable_events = []
        if usage.unlock_count > 100:
            notable_events.append("Very active day with lots of unlocks")
        if usage.total_screen_time > 360:
            notable_events.append("Heavy usage day")
        
        # Get top apps used today
        top_app_usage = AppUsage.objects.filter(
            device_app__device=device,
            date=date
        ).order_by('-time_spent_minutes')[:3]
        
        top_apps = [au.device_app for au in top_app_usage]
        
        # Generate journal
        ai_result = AIGenerationService.generate_device_journal(
            device=device,
            date=date,
            usage_summary=usage_summary,
            notable_events=notable_events,
            mentioned_apps=list(top_apps)
        )
        
        if ai_result['success']:
            DeviceJournal.objects.create(
                device=device,
                date=date,
                content=ai_result['content'],
                mood='satisfied',  # Valid choice from model
                generation_prompt=ai_result['generation_prompt'],
                ai_generated=True  # Correct field name
            )
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"Error generating device journal: {str(e)}")
        return False


def generate_app_journal_entry(device_app, date):
    """Generate a journal entry for an app"""
    try:
        # Get usage stats for this app
        app_usage = AppUsage.objects.filter(
            device_app=device_app,
            date=date
        ).first()
        
        if not app_usage:
            return False
        
        usage_stats = {
            'time_spent': app_usage.time_spent_minutes,
            'launch_count': app_usage.launch_count
        }
        
        session_highlights = []
        if app_usage.time_spent_minutes > 120:
            session_highlights.append("Power user session")
        if app_usage.launch_count > 20:
            session_highlights.append("Frequently opened")
        
        # Generate journal
        ai_result = AIGenerationService.generate_app_journal(
            device_app=device_app,
            date=date,
            usage_stats=usage_stats,
            session_highlights=session_highlights
        )
        
        if ai_result['success']:
            AppJournal.objects.create(
                device_app=device_app,
                date=date,
                content=ai_result['content'],
                mood='satisfied',  # Valid choice from model
                generation_prompt=ai_result['generation_prompt'],
                ai_generated=True  # Correct field name
            )
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"Error generating app journal: {str(e)}")
        return False


@shared_task(name='apps.ai_engine.tasks.generate_conversation_on_demand')
def generate_conversation_on_demand(user_id, conversation_type='daily_recap', mood='humorous'):
    """
    Generate a conversation on demand for a specific user
    Can be triggered manually or by specific events
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        user = User.objects.get(id=user_id)
        date = timezone.now().date()
        
        result = generate_conversation_for_user(user, date)
        return {'success': result, 'user_id': user_id}
        
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return {'success': False, 'error': 'User not found'}
    except Exception as e:
        logger.error(f"Error in on-demand conversation generation: {str(e)}")
        return {'success': False, 'error': str(e)}
