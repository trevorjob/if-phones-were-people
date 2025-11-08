"""
Celery tasks for usage pattern detection and analysis
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta, datetime, time
from django.db.models import Sum, Avg, Count, Q
from apps.usage.models import UsageData, AppUsageData, UsagePattern
from apps.devices.models import Device
import logging

logger = logging.getLogger('usage')


@shared_task(name='apps.usage.tasks.detect_patterns')
def detect_patterns():
    """
    Detect usage patterns for all users
    Runs daily at 12:30 AM
    """
    logger.info("Starting usage pattern detection")
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    detected_count = 0
    users = User.objects.filter(devices__is_active=True).distinct()
    
    for user in users:
        try:
            patterns = detect_patterns_for_user(user)
            detected_count += len(patterns)
        except Exception as e:
            logger.error(f"Error detecting patterns for user {user.id}: {str(e)}")
    
    logger.info(f"Pattern detection complete: {detected_count} patterns detected")
    return {'patterns_detected': detected_count}


def detect_patterns_for_user(user):
    """Detect various usage patterns for a user"""
    detected_patterns = []
    now = timezone.now()
    
    # Get usage data for last 7 days
    week_ago = now - timedelta(days=7)
    usage_data = UsageData.objects.filter(
        device__user=user,
        date__gte=week_ago.date()
    )
    
    if not usage_data.exists():
        return detected_patterns
    
    # Check for various patterns
    detected_patterns.extend(check_binge_pattern(user, usage_data))
    detected_patterns.extend(check_night_owl_pattern(user, usage_data))
    detected_patterns.extend(check_morning_person_pattern(user, usage_data))
    detected_patterns.extend(check_weekend_warrior_pattern(user, usage_data))
    detected_patterns.extend(check_distracted_pattern(user, usage_data))
    detected_patterns.extend(check_doom_scrolling_pattern(user, usage_data))
    detected_patterns.extend(check_phantom_vibration_pattern(user, usage_data))
    detected_patterns.extend(check_app_switching_pattern(user, usage_data))
    detected_patterns.extend(check_notification_addiction_pattern(user, usage_data))
    
    return detected_patterns


def check_binge_pattern(user, usage_data):
    """Check for binge usage pattern (extended sessions)"""
    patterns = []
    
    # Look for days with 5+ hours of continuous usage
    high_usage_days = usage_data.filter(total_screen_time__gte=300)  # 5+ hours
    
    if high_usage_days.count() >= 3:  # 3 or more days in the week
        pattern, created = UsagePattern.objects.get_or_create(
            user=user,
            pattern_type='binge_usage',
            defaults={
                'description': 'Frequent extended usage sessions detected',
                'severity': 'medium',
                'confidence': 0.8,
                'metadata': {
                    'days_count': high_usage_days.count(),
                    'avg_screen_time': high_usage_days.aggregate(Avg('total_screen_time'))['total_screen_time__avg']
                }
            }
        )
        patterns.append(pattern)
    
    return patterns


def check_night_owl_pattern(user, usage_data):
    """Check for late night usage pattern"""
    patterns = []
    
    # Count late night usage (after 11 PM)
    late_night_count = 0
    for data in usage_data:
        # Check if there's significant usage data late at night
        # This would require more granular timestamp data
        # For now, we'll use a simplified check
        pass
    
    # Simplified: check if average last_used time is late
    recent_devices = Device.objects.filter(user=user, is_active=True)
    late_night_devices = 0
    
    for device in recent_devices:
        if device.last_used and device.last_used.hour >= 23:
            late_night_devices += 1
    
    if late_night_devices >= 1:
        pattern, created = UsagePattern.objects.get_or_create(
            user=user,
            pattern_type='night_owl',
            defaults={
                'description': 'Regular late-night device usage detected',
                'severity': 'low',
                'confidence': 0.6,
                'metadata': {'devices_count': late_night_devices}
            }
        )
        patterns.append(pattern)
    
    return patterns


def check_morning_person_pattern(user, usage_data):
    """Check for early morning usage pattern"""
    patterns = []
    
    # Similar to night owl, check for early morning usage
    recent_devices = Device.objects.filter(user=user, is_active=True)
    morning_devices = 0
    
    for device in recent_devices:
        if device.last_used and 5 <= device.last_used.hour <= 7:
            morning_devices += 1
    
    if morning_devices >= 1:
        pattern, created = UsagePattern.objects.get_or_create(
            user=user,
            pattern_type='morning_person',
            defaults={
                'description': 'Regular early morning device usage detected',
                'severity': 'low',
                'confidence': 0.6,
                'metadata': {'devices_count': morning_devices}
            }
        )
        patterns.append(pattern)
    
    return patterns


def check_weekend_warrior_pattern(user, usage_data):
    """Check for increased weekend usage"""
    patterns = []
    
    # Compare weekday vs weekend usage
    weekday_usage = usage_data.filter(
        date__week_day__in=[2, 3, 4, 5, 6]  # Mon-Fri (Django week_day)
    ).aggregate(
        avg_time=Avg('total_screen_time')
    )['avg_time'] or 0
    
    weekend_usage = usage_data.filter(
        date__week_day__in=[1, 7]  # Sat-Sun
    ).aggregate(
        avg_time=Avg('total_screen_time')
    )['avg_time'] or 0
    
    # Weekend usage is 50% higher than weekday
    if weekend_usage > weekday_usage * 1.5 and weekday_usage > 0:
        pattern, created = UsagePattern.objects.get_or_create(
            user=user,
            pattern_type='weekend_warrior',
            defaults={
                'description': 'Significantly higher usage on weekends',
                'severity': 'low',
                'confidence': 0.7,
                'metadata': {
                    'weekday_avg': round(weekday_usage, 1),
                    'weekend_avg': round(weekend_usage, 1),
                    'increase_percent': round((weekend_usage - weekday_usage) / weekday_usage * 100, 1)
                }
            }
        )
        patterns.append(pattern)
    
    return patterns


def check_distracted_pattern(user, usage_data):
    """Check for distraction pattern (frequent unlocks, short sessions)"""
    patterns = []
    
    # High unlock count but relatively low total screen time
    avg_unlocks = usage_data.aggregate(Avg('unlock_count'))['unlock_count__avg'] or 0
    avg_screen_time = usage_data.aggregate(Avg('total_screen_time'))['total_screen_time__avg'] or 0
    
    if avg_unlocks > 80 and avg_screen_time < 180:  # 80+ unlocks, less than 3 hours
        pattern, created = UsagePattern.objects.get_or_create(
            user=user,
            pattern_type='distracted',
            defaults={
                'description': 'Frequent phone checks with short sessions',
                'severity': 'medium',
                'confidence': 0.75,
                'metadata': {
                    'avg_unlocks': round(avg_unlocks, 1),
                    'avg_screen_time': round(avg_screen_time, 1),
                    'avg_session_length': round(avg_screen_time / avg_unlocks, 2) if avg_unlocks > 0 else 0
                }
            }
        )
        patterns.append(pattern)
    
    return patterns


def check_doom_scrolling_pattern(user, usage_data):
    """Check for doom scrolling (long sessions on social/news apps)"""
    patterns = []
    
    # Get social media and news app usage
    social_categories = ['Social', 'News', 'Entertainment']
    
    social_usage = AppUsageData.objects.filter(
        usage_data__in=usage_data,
        device_app__app__category__name__in=social_categories
    ).aggregate(
        total_time=Sum('time_spent'),
        avg_session=Avg('time_spent')
    )
    
    total_social_time = social_usage['total_time'] or 0
    avg_session = social_usage['avg_session'] or 0
    
    # High social media usage with long sessions
    if total_social_time > 600 and avg_session > 30:  # 10+ hours total, 30+ min sessions
        pattern, created = UsagePattern.objects.get_or_create(
            user=user,
            pattern_type='doom_scrolling',
            defaults={
                'description': 'Extended social media and content scrolling sessions',
                'severity': 'high',
                'confidence': 0.8,
                'metadata': {
                    'total_social_time': round(total_social_time, 1),
                    'avg_session_length': round(avg_session, 1)
                }
            }
        )
        patterns.append(pattern)
    
    return patterns


def check_phantom_vibration_pattern(user, usage_data):
    """Check for phantom vibration pattern (unlocking with no notifications)"""
    patterns = []
    
    # High unlock count
    high_unlock_days = usage_data.filter(unlock_count__gte=100).count()
    
    if high_unlock_days >= 4:  # 4 or more days with 100+ unlocks
        pattern, created = UsagePattern.objects.get_or_create(
            user=user,
            pattern_type='phantom_vibration',
            defaults={
                'description': 'Frequent unlocking behavior detected',
                'severity': 'medium',
                'confidence': 0.65,
                'metadata': {'high_unlock_days': high_unlock_days}
            }
        )
        patterns.append(pattern)
    
    return patterns


def check_app_switching_pattern(user, usage_data):
    """Check for app switching pattern (using many different apps)"""
    patterns = []
    
    # Count unique apps used per day
    for data in usage_data:
        app_count = AppUsageData.objects.filter(usage_data=data).count()
        if app_count > 30:  # Using 30+ different apps in a day
            pattern, created = UsagePattern.objects.get_or_create(
                user=user,
                pattern_type='app_switching',
                defaults={
                    'description': 'Frequent switching between multiple apps',
                    'severity': 'low',
                    'confidence': 0.7,
                    'metadata': {'max_apps_per_day': app_count}
                }
            )
            patterns.append(pattern)
            break  # Only create once
    
    return patterns


def check_notification_addiction_pattern(user, usage_data):
    """Check for notification addiction (quick response to unlocks)"""
    patterns = []
    
    # Very high unlock count consistently
    avg_unlocks = usage_data.aggregate(Avg('unlock_count'))['unlock_count__avg'] or 0
    
    if avg_unlocks > 120:  # 120+ unlocks per day on average
        pattern, created = UsagePattern.objects.get_or_create(
            user=user,
            pattern_type='notification_addiction',
            defaults={
                'description': 'Very frequent device checking behavior',
                'severity': 'high',
                'confidence': 0.85,
                'metadata': {'avg_daily_unlocks': round(avg_unlocks, 1)}
            }
        )
        patterns.append(pattern)
    
    return patterns


@shared_task(name='apps.usage.tasks.cleanup_old_usage_data')
def cleanup_old_usage_data():
    """
    Clean up old usage data (keep last 90 days)
    Runs weekly on Sunday at 2 AM
    """
    logger.info("Starting usage data cleanup")
    
    cutoff_date = timezone.now().date() - timedelta(days=90)
    
    # Delete old usage data
    deleted_usage = UsageData.objects.filter(date__lt=cutoff_date).delete()
    
    # Delete resolved patterns older than 30 days
    pattern_cutoff = timezone.now() - timedelta(days=30)
    deleted_patterns = UsagePattern.objects.filter(
        resolved=True,
        last_detected__lt=pattern_cutoff
    ).delete()
    
    logger.info(f"Cleanup complete: {deleted_usage[0]} usage records, {deleted_patterns[0]} patterns deleted")
    
    return {
        'usage_deleted': deleted_usage[0],
        'patterns_deleted': deleted_patterns[0],
        'cutoff_date': str(cutoff_date)
    }
