"""
Celery configuration for if_phones_were_people project
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'if_phones_were_people.settings')

app = Celery('if_phones_were_people')

# Load config from Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'generate-daily-conversations': {
        'task': 'apps.ai_engine.tasks.generate_daily_conversations',
        'schedule': crontab(hour=6, minute=0),  # 6 AM daily
    },
    'detect-usage-patterns': {
        'task': 'apps.usage.tasks.detect_patterns',
        'schedule': crontab(hour=0, minute=30),  # 12:30 AM daily
    },
    'calculate-analytics': {
        'task': 'apps.analytics.tasks.calculate_user_stats',
        'schedule': crontab(hour=1, minute=0),  # 1 AM daily
    },
    'generate-device-journals': {
        'task': 'apps.ai_engine.tasks.generate_daily_journals',
        'schedule': crontab(hour=23, minute=0),  # 11 PM daily
    },
    'cleanup-old-data': {
        'task': 'apps.usage.tasks.cleanup_old_usage_data',
        'schedule': crontab(hour=2, minute=0, day_of_week=0),  # Weekly on Sunday at 2 AM
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')
