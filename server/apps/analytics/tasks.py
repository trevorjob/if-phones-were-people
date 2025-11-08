"""
Celery tasks for analytics calculation
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Avg, Count, Max, F, Q
from apps.analytics.models import UserStats, TrendAnalysis
from apps.usage.models import UsageData, AppUsageData, UsagePattern
from apps.conversations.models import Conversation
from apps.devices.models import Device
from apps.social.models import FriendConnection, Challenge
import logging

logger = logging.getLogger('analytics')


@shared_task(name='apps.analytics.tasks.calculate_user_stats')
def calculate_user_stats():
    """
    Calculate statistics for all users
    Runs daily at 1 AM
    """
    logger.info("Starting user statistics calculation")
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    updated_count = 0
    users = User.objects.filter(is_active=True)
    
    for user in users:
        try:
            calculate_stats_for_user(user)
            updated_count += 1
        except Exception as e:
            logger.error(f"Error calculating stats for user {user.id}: {str(e)}")
    
    logger.info(f"User statistics calculation complete: {updated_count} users updated")
    
    # Also calculate trends
    calculate_trends()
    
    return {'users_updated': updated_count}


def calculate_stats_for_user(user):
    """Calculate comprehensive statistics for a user"""
    now = timezone.now()
    today = now.date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Get or create UserStats
    stats, created = UserStats.objects.get_or_create(user=user)
    
    # Total screen time
    total_usage = UsageData.objects.filter(device__user=user).aggregate(
        total=Sum('total_screen_time')
    )['total'] or 0
    
    stats.total_screen_time = total_usage
    
    # Total unlocks
    total_unlocks = UsageData.objects.filter(device__user=user).aggregate(
        total=Sum('unlock_count')
    )['total'] or 0
    
    stats.total_unlocks = total_unlocks
    
    # Total conversations
    stats.total_conversations = Conversation.objects.filter(user=user).count()
    
    # Conversations read
    stats.conversations_read = Conversation.objects.filter(
        user=user,
        is_read=True
    ).count()
    
    # Active days
    stats.active_days = UsageData.objects.filter(
        device__user=user
    ).values('date').distinct().count()
    
    # Current streak
    stats.current_streak = calculate_current_streak(user)
    
    # Longest streak
    longest = calculate_longest_streak(user)
    if longest > stats.longest_streak:
        stats.longest_streak = longest
    
    # Average daily screen time (last 30 days)
    recent_usage = UsageData.objects.filter(
        device__user=user,
        date__gte=month_ago
    ).aggregate(avg=Avg('total_screen_time'))['avg'] or 0
    
    stats.avg_daily_screen_time = round(recent_usage, 1)
    
    # Average daily unlocks (last 30 days)
    recent_unlocks = UsageData.objects.filter(
        device__user=user,
        date__gte=month_ago
    ).aggregate(avg=Avg('unlock_count'))['avg'] or 0
    
    stats.avg_daily_unlocks = round(recent_unlocks, 1)
    
    # Most used app
    top_app = AppUsageData.objects.filter(
        usage_data__device__user=user,
        usage_data__date__gte=month_ago
    ).values('device_app__app__name').annotate(
        total_time=Sum('time_spent')
    ).order_by('-total_time').first()
    
    if top_app:
        stats.most_used_app = top_app['device_app__app__name']
        stats.most_used_app_time = top_app['total_time']
    
    # Most productive app
    productive_app = AppUsageData.objects.filter(
        usage_data__device__user=user,
        usage_data__date__gte=month_ago,
        device_app__app__category__name='Productivity'
    ).values('device_app__app__name').annotate(
        total_time=Sum('time_spent')
    ).order_by('-total_time').first()
    
    if productive_app:
        stats.most_productive_app = productive_app['device_app__app__name']
    
    # Favorite device
    favorite_device = Device.objects.filter(
        user=user,
        is_active=True
    ).annotate(
        usage_count=Count('usage_data')
    ).order_by('-usage_count').first()
    
    if favorite_device:
        stats.favorite_device = favorite_device.name
    
    # Active patterns count
    stats.active_patterns = UsagePattern.objects.filter(
        user=user,
        resolved=False
    ).count()
    
    # Friends count
    stats.friends_count = FriendConnection.objects.filter(
        Q(user=user) | Q(friend=user),
        status='accepted'
    ).count()
    
    # Challenges completed
    stats.challenges_completed = user.challenge_participants.filter(
        status='completed'
    ).count()
    
    # Achievements earned (placeholder - would need achievement system)
    stats.achievements_earned = 0  # TODO: Implement achievement system
    
    # Goals achieved
    from apps.usage.models import UsageGoal
    stats.goals_achieved = UsageGoal.objects.filter(
        user=user,
        status='achieved'
    ).count()
    
    # Week comparison (this week vs last week)
    this_week_start = today - timedelta(days=today.weekday())
    last_week_start = this_week_start - timedelta(days=7)
    last_week_end = this_week_start - timedelta(days=1)
    
    this_week_usage = UsageData.objects.filter(
        device__user=user,
        date__gte=this_week_start
    ).aggregate(total=Sum('total_screen_time'))['total'] or 0
    
    last_week_usage = UsageData.objects.filter(
        device__user=user,
        date__gte=last_week_start,
        date__lte=last_week_end
    ).aggregate(total=Sum('total_screen_time'))['total'] or 0
    
    if last_week_usage > 0:
        percent_change = ((this_week_usage - last_week_usage) / last_week_usage) * 100
        stats.week_comparison = round(percent_change, 1)
    else:
        stats.week_comparison = 0.0
    
    # Month comparison
    this_month_start = today.replace(day=1)
    if this_month_start.month == 1:
        last_month_start = this_month_start.replace(year=this_month_start.year - 1, month=12)
    else:
        last_month_start = this_month_start.replace(month=this_month_start.month - 1)
    
    last_month_end = this_month_start - timedelta(days=1)
    
    this_month_usage = UsageData.objects.filter(
        device__user=user,
        date__gte=this_month_start
    ).aggregate(total=Sum('total_screen_time'))['total'] or 0
    
    last_month_usage = UsageData.objects.filter(
        device__user=user,
        date__gte=last_month_start,
        date__lte=last_month_end
    ).aggregate(total=Sum('total_screen_time'))['total'] or 0
    
    if last_month_usage > 0:
        percent_change = ((this_month_usage - last_month_usage) / last_month_usage) * 100
        stats.month_comparison = round(percent_change, 1)
    else:
        stats.month_comparison = 0.0
    
    # Peak usage day
    peak_day = UsageData.objects.filter(
        device__user=user
    ).order_by('-total_screen_time').first()
    
    if peak_day:
        stats.peak_usage_day = peak_day.date
        stats.peak_usage_amount = peak_day.total_screen_time
    
    # Wellness score (0-100, higher is better)
    stats.wellness_score = calculate_wellness_score(user, stats)
    
    stats.save()
    
    logger.info(f"Updated stats for user {user.id}")


def calculate_current_streak(user):
    """Calculate current consecutive days of usage"""
    today = timezone.now().date()
    streak = 0
    
    check_date = today
    while True:
        has_usage = UsageData.objects.filter(
            device__user=user,
            date=check_date
        ).exists()
        
        if not has_usage:
            break
        
        streak += 1
        check_date -= timedelta(days=1)
        
        # Limit check to avoid infinite loop
        if streak > 365:
            break
    
    return streak


def calculate_longest_streak(user):
    """Calculate longest streak of consecutive days"""
    # Get all dates with usage
    usage_dates = UsageData.objects.filter(
        device__user=user
    ).values_list('date', flat=True).distinct().order_by('date')
    
    if not usage_dates:
        return 0
    
    dates = list(usage_dates)
    longest = 1
    current = 1
    
    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    
    return longest


def calculate_wellness_score(user, stats):
    """
    Calculate wellness score based on various factors
    100 = perfect, 0 = concerning
    """
    score = 100
    
    # Screen time penalty (lose up to 30 points)
    if stats.avg_daily_screen_time > 360:  # 6+ hours
        score -= 30
    elif stats.avg_daily_screen_time > 240:  # 4-6 hours
        score -= 20
    elif stats.avg_daily_screen_time > 180:  # 3-4 hours
        score -= 10
    
    # Unlock frequency penalty (lose up to 20 points)
    if stats.avg_daily_unlocks > 150:
        score -= 20
    elif stats.avg_daily_unlocks > 100:
        score -= 10
    
    # Active patterns penalty (lose up to 20 points)
    if stats.active_patterns > 5:
        score -= 20
    elif stats.active_patterns > 3:
        score -= 10
    elif stats.active_patterns > 0:
        score -= 5
    
    # Goals bonus (add up to 15 points)
    if stats.goals_achieved > 10:
        score += 15
    elif stats.goals_achieved > 5:
        score += 10
    elif stats.goals_achieved > 0:
        score += 5
    
    # Streak bonus (add up to 15 points)
    if stats.current_streak > 30:
        score += 15
    elif stats.current_streak > 14:
        score += 10
    elif stats.current_streak > 7:
        score += 5
    
    return max(0, min(100, score))  # Clamp between 0-100


def calculate_trends():
    """Calculate trend analyses"""
    logger.info("Starting trend analysis")
    
    today = timezone.now().date()
    
    # Popular apps trend
    calculate_popular_apps_trend(today)
    
    # Usage patterns trend
    calculate_usage_patterns_trend(today)
    
    # Conversation topics trend
    calculate_conversation_topics_trend(today)
    
    logger.info("Trend analysis complete")


def calculate_popular_apps_trend(date):
    """Calculate most popular apps"""
    week_ago = date - timedelta(days=7)
    
    # Get top apps by total usage
    top_apps = AppUsageData.objects.filter(
        usage_data__date__gte=week_ago
    ).values('device_app__app__name').annotate(
        total_time=Sum('time_spent'),
        user_count=Count('usage_data__device__user', distinct=True)
    ).order_by('-total_time')[:10]
    
    trend_data = {
        'top_apps': list(top_apps),
        'period': 'weekly'
    }
    
    TrendAnalysis.objects.update_or_create(
        trend_type='popular_apps',
        period='weekly',
        defaults={
            'data': trend_data,
            'date': date
        }
    )


def calculate_usage_patterns_trend(date):
    """Calculate trending usage patterns"""
    week_ago = date - timedelta(days=7)
    
    # Get pattern distribution
    patterns = UsagePattern.objects.filter(
        first_detected__gte=week_ago
    ).values('pattern_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    trend_data = {
        'patterns': list(patterns),
        'period': 'weekly'
    }
    
    TrendAnalysis.objects.update_or_create(
        trend_type='usage_patterns',
        period='weekly',
        defaults={
            'data': trend_data,
            'date': date
        }
    )


def calculate_conversation_topics_trend(date):
    """Calculate trending conversation topics"""
    week_ago = date - timedelta(days=7)
    
    # Get conversation types distribution
    conversations = Conversation.objects.filter(
        created_at__gte=week_ago
    ).values('conversation_type', 'mood').annotate(
        count=Count('id')
    ).order_by('-count')
    
    trend_data = {
        'topics': list(conversations),
        'period': 'weekly'
    }
    
    TrendAnalysis.objects.update_or_create(
        trend_type='conversation_topics',
        period='weekly',
        defaults={
            'data': trend_data,
            'date': date
        }
    )
