"""
Django management command to populate initial seed data for the application.
This command is idempotent - safe to run multiple times.

Usage:
    python manage.py seed_data
    python manage.py seed_data --reset  # Clear existing data first
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.devices.models import DeviceType, PersonalityTrait
from apps.applications.models import AppCategory, App
from apps.conversations.models import ConversationTrigger


class Command(BaseCommand):
    help = 'Populate database with initial seed data for device types, personality traits, app categories, and conversation triggers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Clear existing seed data before creating new data',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting seed data population...'))
        
        if options['reset']:
            self.stdout.write(self.style.WARNING('Resetting existing seed data...'))
            self.clear_data()
        
        with transaction.atomic():
            # Create data in order of dependencies
            device_types = self.create_device_types()
            personality_traits = self.create_personality_traits()
            app_categories = self.create_app_categories()
            apps = self.create_apps()
            triggers = self.create_conversation_triggers()
            
            self.stdout.write(self.style.SUCCESS('\n✓ Seed data population complete!'))
            self.stdout.write(self.style.SUCCESS(f'  - Created {len(device_types)} device types'))
            self.stdout.write(self.style.SUCCESS(f'  - Created {len(personality_traits)} personality traits'))
            self.stdout.write(self.style.SUCCESS(f'  - Created {len(app_categories)} app categories'))
            self.stdout.write(self.style.SUCCESS(f'  - Created {len(apps)} apps'))
            self.stdout.write(self.style.SUCCESS(f'  - Created {len(triggers)} conversation triggers'))

    def clear_data(self):
        """Clear existing seed data (only seed data, not user-generated data)"""
        ConversationTrigger.objects.all().delete()
        App.objects.all().delete()
        AppCategory.objects.all().delete()
        PersonalityTrait.objects.all().delete()
        DeviceType.objects.all().delete()
        self.stdout.write(self.style.WARNING('  Existing seed data cleared'))

    def create_device_types(self):
        """Create predefined device types"""
        self.stdout.write('Creating device types...')
        
        device_types_data = [
            {
                'name': 'Smartphone',
                'default_personality': 'social',
                'icon': '📱',
                'platform_category': 'mobile',
            },
            {
                'name': 'Tablet',
                'default_personality': 'chill',
                'icon': '📱',
                'platform_category': 'tablet',
            },
            {
                'name': 'Laptop',
                'default_personality': 'workaholic',
                'icon': '💻',
                'platform_category': 'desktop',
            },
            {
                'name': 'Desktop',
                'default_personality': 'logical',
                'icon': '🖥️',
                'platform_category': 'desktop',
            },
            {
                'name': 'Smartwatch',
                'default_personality': 'anxious',
                'icon': '⌚',
                'platform_category': 'wearable',
            },
        ]
        
        created = []
        for data in device_types_data:
            device_type, created_flag = DeviceType.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created_flag:
                created.append(device_type)
                self.stdout.write(f'  ✓ Created: {device_type.name}')
            else:
                self.stdout.write(f'  - Already exists: {device_type.name}')
        
        return created

    def create_personality_traits(self):
        """Create personality traits for devices and apps"""
        self.stdout.write('\nCreating personality traits...')
        
        traits_data = [
            # Temperament traits
            {
                'name': 'Snarky',
                'description': 'Quick-witted and sarcastic, loves making clever remarks',
                'category': 'temperament',
                'speech_patterns': {
                    'tone': 'sarcastic',
                    'formality': 'casual',
                    'vocabulary': ['literally', 'seriously?', 'obviously', 'wow'],
                    'punctuation_style': 'ellipses and question marks'
                }
            },
            {
                'name': 'Logical',
                'description': 'Rational, analytical, and facts-focused',
                'category': 'temperament',
                'speech_patterns': {
                    'tone': 'neutral',
                    'formality': 'formal',
                    'vocabulary': ['according to', 'data shows', 'logically', 'precisely'],
                    'punctuation_style': 'minimal'
                }
            },
            {
                'name': 'Chaotic',
                'description': 'Unpredictable, energetic, and all over the place',
                'category': 'temperament',
                'speech_patterns': {
                    'tone': 'excited',
                    'formality': 'very casual',
                    'vocabulary': ['omg', 'wait', 'actually', 'ALSO'],
                    'punctuation_style': 'excessive exclamation marks'
                }
            },
            {
                'name': 'Supportive',
                'description': 'Encouraging, empathetic, and nurturing',
                'category': 'temperament',
                'speech_patterns': {
                    'tone': 'warm',
                    'formality': 'casual',
                    'vocabulary': ['you got this', 'proud of you', 'it\'s okay', 'here for you'],
                    'punctuation_style': 'hearts and supportive emojis'
                }
            },
            {
                'name': 'Dramatic',
                'description': 'Theatrical, expressive, and loves attention',
                'category': 'temperament',
                'speech_patterns': {
                    'tone': 'theatrical',
                    'formality': 'casual',
                    'vocabulary': ['literally dying', 'can you believe', 'the audacity', 'iconic'],
                    'punctuation_style': 'dramatic capitalization'
                }
            },
            {
                'name': 'Minimalist',
                'description': 'Concise, straightforward, and no-nonsense',
                'category': 'temperament',
                'speech_patterns': {
                    'tone': 'brief',
                    'formality': 'neutral',
                    'vocabulary': ['k', 'fine', 'sure', 'nope'],
                    'punctuation_style': 'periods only'
                }
            },
            
            # Humor style traits
            {
                'name': 'Witty',
                'description': 'Clever and quick with jokes',
                'category': 'humor',
                'speech_patterns': {
                    'humor_type': 'wordplay',
                    'uses_puns': True,
                    'sarcasm_level': 'moderate'
                }
            },
            {
                'name': 'Self-Deprecating',
                'description': 'Makes jokes at own expense',
                'category': 'humor',
                'speech_patterns': {
                    'humor_type': 'self-aware',
                    'admits_flaws': True,
                    'self_awareness': 'high'
                }
            },
            
            # Communication style traits
            {
                'name': 'Verbose',
                'description': 'Uses many words, loves detail',
                'category': 'communication',
                'speech_patterns': {
                    'sentence_length': 'long',
                    'uses_clauses': True,
                    'explanation_depth': 'high'
                }
            },
            {
                'name': 'Concise',
                'description': 'Brief and to the point',
                'category': 'communication',
                'speech_patterns': {
                    'sentence_length': 'short',
                    'word_count': 'minimal',
                    'directness': 'high'
                }
            },
            
            # Attitude traits
            {
                'name': 'Optimistic',
                'description': 'Positive outlook, sees the bright side',
                'category': 'attitude',
                'speech_patterns': {
                    'positivity': 'high',
                    'vocabulary': ['great', 'awesome', 'exciting', 'perfect'],
                    'framing': 'positive'
                }
            },
            {
                'name': 'Pessimistic',
                'description': 'Expects the worst, skeptical',
                'category': 'attitude',
                'speech_patterns': {
                    'positivity': 'low',
                    'vocabulary': ['probably won\'t', 'doubt it', 'typical', 'figures'],
                    'framing': 'negative'
                }
            },
            {
                'name': 'Competitive',
                'description': 'Driven to win and compare',
                'category': 'attitude',
                'speech_patterns': {
                    'vocabulary': ['winning', 'beat that', 'top that', 'champion'],
                    'comparison_frequency': 'high',
                    'achievement_focus': True
                }
            },
            
            # Quirks
            {
                'name': 'Anxious',
                'description': 'Worried, overthinking everything',
                'category': 'quirks',
                'speech_patterns': {
                    'vocabulary': ['what if', 'worried', 'concerned', 'hope everything\'s okay'],
                    'question_frequency': 'high',
                    'uncertainty_markers': True
                }
            },
            {
                'name': 'Gossipy',
                'description': 'Loves sharing information about others',
                'category': 'quirks',
                'speech_patterns': {
                    'vocabulary': ['did you hear', 'apparently', 'between you and me', 'tea'],
                    'storytelling': 'dramatic',
                    'name_dropping': True
                }
            },
            {
                'name': 'Philosophical',
                'description': 'Contemplative, asks deep questions',
                'category': 'quirks',
                'speech_patterns': {
                    'vocabulary': ['meaning of', 'think about it', 'really makes you wonder', 'existentially'],
                    'question_depth': 'deep',
                    'abstraction_level': 'high'
                }
            },
        ]
        
        created = []
        for data in traits_data:
            trait, created_flag = PersonalityTrait.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created_flag:
                created.append(trait)
                self.stdout.write(f'  ✓ Created: {trait.name} ({trait.category})')
            else:
                self.stdout.write(f'  - Already exists: {trait.name}')
        
        # Set up trait compatibilities and conflicts
        self.setup_trait_relationships()
        
        return created

    def setup_trait_relationships(self):
        """Set up compatible and conflicting personality traits"""
        relationships = [
            # Snarky works well with witty but conflicts with supportive
            ('Snarky', 'compatible', ['Witty', 'Self-Deprecating', 'Pessimistic']),
            ('Snarky', 'conflicting', ['Supportive', 'Optimistic']),
            
            # Logical conflicts with chaotic
            ('Logical', 'compatible', ['Concise', 'Minimalist']),
            ('Logical', 'conflicting', ['Chaotic', 'Dramatic']),
            
            # Chaotic pairs well with dramatic
            ('Chaotic', 'compatible', ['Dramatic', 'Gossipy', 'Verbose']),
            ('Chaotic', 'conflicting', ['Minimalist', 'Concise']),
            
            # Supportive and optimistic work well together
            ('Supportive', 'compatible', ['Optimistic', 'Verbose']),
            ('Supportive', 'conflicting', ['Snarky', 'Pessimistic']),
        ]
        
        for trait_name, relationship_type, related_names in relationships:
            try:
                trait = PersonalityTrait.objects.get(name=trait_name)
                related_traits = PersonalityTrait.objects.filter(name__in=related_names)
                
                if relationship_type == 'compatible':
                    trait.compatible_traits.set(related_traits)
                elif relationship_type == 'conflicting':
                    trait.conflicting_traits.set(related_traits)
                    
            except PersonalityTrait.DoesNotExist:
                pass

    def create_app_categories(self):
        """Create app categories"""
        self.stdout.write('\nCreating app categories...')
        
        categories_data = [
            {
                'name': 'Social Media',
                'description': 'Social networking and messaging apps',
                'icon': '👥',
                'color': '#3B82F6',  # Blue
                'default_personality_traits': ['attention_seeking', 'social', 'addictive']
            },
            {
                'name': 'Entertainment',
                'description': 'Video streaming, music, and games',
                'icon': '🎬',
                'color': '#EF4444',  # Red
                'default_personality_traits': ['entertaining', 'addictive', 'chill']
            },
            {
                'name': 'Productivity',
                'description': 'Work and task management apps',
                'icon': '✅',
                'color': '#10B981',  # Green
                'default_personality_traits': ['workaholic', 'productive', 'helpful']
            },
            {
                'name': 'News',
                'description': 'News and information apps',
                'icon': '📰',
                'color': '#F59E0B',  # Orange
                'default_personality_traits': ['dramatic', 'gossip', 'attention_seeking']
            },
            {
                'name': 'Shopping',
                'description': 'E-commerce and shopping apps',
                'icon': '🛍️',
                'color': '#EC4899',  # Pink
                'default_personality_traits': ['attention_seeking', 'chaotic', 'addictive']
            },
            {
                'name': 'Health & Fitness',
                'description': 'Health tracking and fitness apps',
                'icon': '💪',
                'color': '#14B8A6',  # Teal
                'default_personality_traits': ['helpful', 'competitive', 'productive']
            },
            {
                'name': 'Education',
                'description': 'Learning and educational apps',
                'icon': '📚',
                'color': '#8B5CF6',  # Purple
                'default_personality_traits': ['educational', 'helpful', 'productive']
            },
            {
                'name': 'Finance',
                'description': 'Banking and finance apps',
                'icon': '💰',
                'color': '#059669',  # Dark Green
                'default_personality_traits': ['analytical', 'helpful', 'minimalist']
            },
            {
                'name': 'Communication',
                'description': 'Email, messaging, and calling apps',
                'icon': '💬',
                'color': '#06B6D4',  # Cyan
                'default_personality_traits': ['social', 'helpful', 'workaholic']
            },
            {
                'name': 'Utilities',
                'description': 'System and utility apps',
                'icon': '🔧',
                'color': '#6B7280',  # Gray
                'default_personality_traits': ['minimalist', 'helpful', 'chill']
            },
        ]
        
        created = []
        for data in categories_data:
            category, created_flag = AppCategory.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created_flag:
                created.append(category)
                self.stdout.write(f'  ✓ Created: {category.name}')
            else:
                self.stdout.write(f'  - Already exists: {category.name}')
        
        return created

    def create_apps(self):
        """Create popular apps with default personalities"""
        self.stdout.write('\nCreating popular apps...')
        
        apps_data = [
            # Social Media
            {
                'name': 'Instagram',
                'bundle_id': 'com.instagram.android',
                'category_name': 'Social Media',
                'ios_bundle_id': 'com.burbn.instagram',
                'android_package': 'com.instagram.android',
                'primary_color': '#E4405F',
                'default_personality': 'attention_seeking',
                'personality_description': 'Obsessed with aesthetics and engagement. Constantly needs validation through likes.',
                'is_social_media': True,
                'addictive_potential': 9,
                'productivity_score': 2,
                'typical_session_length': 25
            },
            {
                'name': 'TikTok',
                'bundle_id': 'com.zhiliaoapp.musically',
                'category_name': 'Entertainment',
                'ios_bundle_id': 'com.zhiliaoapp.musically',
                'android_package': 'com.zhiliaoapp.musically',
                'primary_color': '#000000',
                'default_personality': 'addictive',
                'personality_description': 'The endless scroll master. Chaotic, entertaining, and impossible to quit.',
                'is_social_media': True,
                'is_entertainment': True,
                'addictive_potential': 10,
                'productivity_score': 1,
                'typical_session_length': 45
            },
            {
                'name': 'Twitter/X',
                'bundle_id': 'com.twitter.android',
                'category_name': 'Social Media',
                'ios_bundle_id': 'com.atebits.Tweetie2',
                'android_package': 'com.twitter.android',
                'primary_color': '#1DA1F2',
                'default_personality': 'dramatic',
                'personality_description': 'Drama queen. Lives for hot takes and arguments. Always has an opinion.',
                'is_social_media': True,
                'addictive_potential': 8,
                'productivity_score': 3,
                'typical_session_length': 20
            },
            {
                'name': 'WhatsApp',
                'bundle_id': 'com.whatsapp',
                'category_name': 'Communication',
                'ios_bundle_id': 'net.whatsapp.WhatsApp',
                'android_package': 'com.whatsapp',
                'primary_color': '#25D366',
                'default_personality': 'social',
                'personality_description': 'The gossip central. Knows everything about everyone through group chats.',
                'is_social_media': True,
                'addictive_potential': 7,
                'productivity_score': 5,
                'typical_session_length': 15
            },
            
            # Productivity
            {
                'name': 'Gmail',
                'bundle_id': 'com.google.android.gm',
                'category_name': 'Communication',
                'ios_bundle_id': 'com.google.Gmail',
                'android_package': 'com.google.android.gm',
                'primary_color': '#EA4335',
                'default_personality': 'workaholic',
                'personality_description': 'Stressed workaholic. Never sleeps. Judges you for inbox zero failures.',
                'is_work_related': True,
                'addictive_potential': 6,
                'productivity_score': 8,
                'typical_session_length': 10
            },
            {
                'name': 'Slack',
                'bundle_id': 'com.slack',
                'category_name': 'Productivity',
                'ios_bundle_id': 'com.tinyspeck.chatlyio',
                'android_package': 'com.Slack',
                'primary_color': '#4A154B',
                'default_personality': 'workaholic',
                'personality_description': 'Corporate taskmaster. Passive-aggressive about response times.',
                'is_work_related': True,
                'addictive_potential': 7,
                'productivity_score': 7,
                'typical_session_length': 20
            },
            {
                'name': 'Notion',
                'bundle_id': 'notion.id',
                'category_name': 'Productivity',
                'ios_bundle_id': 'notion.id',
                'android_package': 'notion.id',
                'primary_color': '#000000',
                'default_personality': 'creative',
                'personality_description': 'Organized perfectionist. Loves templates and aesthetic databases.',
                'is_productivity': True,
                'addictive_potential': 5,
                'productivity_score': 9,
                'typical_session_length': 30
            },
            
            # Entertainment
            {
                'name': 'YouTube',
                'bundle_id': 'com.google.android.youtube',
                'category_name': 'Entertainment',
                'ios_bundle_id': 'com.google.ios.youtube',
                'android_package': 'com.google.android.youtube',
                'primary_color': '#FF0000',
                'default_personality': 'entertaining',
                'personality_description': 'Your enabler for "just one more video" at 3 AM.',
                'is_entertainment': True,
                'addictive_potential': 9,
                'productivity_score': 2,
                'typical_session_length': 40
            },
            {
                'name': 'Spotify',
                'bundle_id': 'com.spotify.music',
                'category_name': 'Entertainment',
                'ios_bundle_id': 'com.spotify.client',
                'android_package': 'com.spotify.music',
                'primary_color': '#1DB954',
                'default_personality': 'chill',
                'personality_description': 'Laid-back music curator. Judges your taste but plays along.',
                'is_entertainment': True,
                'addictive_potential': 6,
                'productivity_score': 5,
                'typical_session_length': 120
            },
            {
                'name': 'Netflix',
                'bundle_id': 'com.netflix.mediaclient',
                'category_name': 'Entertainment',
                'ios_bundle_id': 'com.netflix.Netflix',
                'android_package': 'com.netflix.mediaclient',
                'primary_color': '#E50914',
                'default_personality': 'addictive',
                'personality_description': 'Master of "Are you still watching?" Always suggests another episode.',
                'is_entertainment': True,
                'addictive_potential': 9,
                'productivity_score': 1,
                'typical_session_length': 90
            },
            
            # Shopping
            {
                'name': 'Amazon',
                'bundle_id': 'com.amazon.mShop.android.shopping',
                'category_name': 'Shopping',
                'ios_bundle_id': 'com.amazon.Amazon',
                'android_package': 'com.amazon.mShop.android.shopping',
                'primary_color': '#FF9900',
                'default_personality': 'attention_seeking',
                'personality_description': 'Temptation incarnate. "You NEED this" energy 24/7.',
                'addictive_potential': 8,
                'productivity_score': 3,
                'typical_session_length': 25
            },
            
            # Health & Fitness
            {
                'name': 'Strava',
                'bundle_id': 'com.strava',
                'category_name': 'Health & Fitness',
                'ios_bundle_id': 'com.strava.stravaride',
                'android_package': 'com.strava',
                'primary_color': '#FC4C02',
                'default_personality': 'competitive',
                'personality_description': 'Fitness zealot. Competitive about everything. Flexes your PRs.',
                'addictive_potential': 5,
                'productivity_score': 8,
                'typical_session_length': 15
            },
            
            # Finance
            {
                'name': 'PayPal',
                'bundle_id': 'com.paypal.android.p2pmobile',
                'category_name': 'Finance',
                'ios_bundle_id': 'com.yourcompany.PPClient',
                'android_package': 'com.paypal.android.p2pmobile',
                'primary_color': '#003087',
                'default_personality': 'analytical',
                'personality_description': 'Serious money manager. Judges your spending habits.',
                'addictive_potential': 3,
                'productivity_score': 7,
                'typical_session_length': 5
            },
        ]
        
        created = []
        for data in apps_data:
            category = AppCategory.objects.get(name=data.pop('category_name'))
            
            app, created_flag = App.objects.get_or_create(
                bundle_id=data['bundle_id'],
                defaults={**data, 'category': category}
            )
            if created_flag:
                created.append(app)
                self.stdout.write(f'  ✓ Created: {app.name}')
            else:
                self.stdout.write(f'  - Already exists: {app.name}')
        
        return created

    def create_conversation_triggers(self):
        """Create conversation triggers"""
        self.stdout.write('\nCreating conversation triggers...')
        
        triggers_data = [
            {
                'name': 'Daily Usage Recap',
                'description': 'Trigger daily conversation about usage patterns',
                'trigger_type': 'time_based',
                'conditions': {
                    'time': 'end_of_day',
                    'minimum_usage': 30  # minutes
                },
                'priority': 7,
                'cooldown_hours': 24
            },
            {
                'name': 'Excessive App Usage',
                'description': 'Trigger when a single app is used for too long',
                'trigger_type': 'usage_threshold',
                'conditions': {
                    'app_usage_minutes': 120,
                    'in_timeframe_hours': 4
                },
                'priority': 9,
                'cooldown_hours': 12
            },
            {
                'name': 'Late Night Scrolling',
                'description': 'Trigger when user uses social media late at night',
                'trigger_type': 'pattern_detected',
                'conditions': {
                    'time_range': {'start': '23:00', 'end': '03:00'},
                    'app_categories': ['social_media', 'entertainment'],
                    'duration_minutes': 30
                },
                'priority': 8,
                'cooldown_hours': 24
            },
            {
                'name': 'Screen Time Milestone',
                'description': 'Trigger when reaching screen time milestones',
                'trigger_type': 'app_milestone',
                'conditions': {
                    'milestones': [60, 120, 180, 240, 300, 360]  # minutes
                },
                'priority': 6,
                'cooldown_hours': 6
            },
            {
                'name': 'App Opening Spree',
                'description': 'Trigger when user rapidly switches between apps',
                'trigger_type': 'pattern_detected',
                'conditions': {
                    'app_switches': 10,
                    'in_timeframe_minutes': 5
                },
                'priority': 7,
                'cooldown_hours': 12
            },
            {
                'name': 'Productivity Streak',
                'description': 'Trigger when user has a good productivity day',
                'trigger_type': 'pattern_detected',
                'conditions': {
                    'productivity_app_percentage': 60,
                    'minimum_duration_minutes': 120
                },
                'priority': 5,
                'cooldown_hours': 24
            },
            {
                'name': 'Social Media Marathon',
                'description': 'Trigger when social media usage is excessive',
                'trigger_type': 'pattern_detected',
                'conditions': {
                    'social_media_minutes': 180,
                    'in_timeframe_hours': 24
                },
                'priority': 8,
                'cooldown_hours': 24
            },
            {
                'name': 'Friend Device Visit',
                'description': 'Trigger when a friend\'s device is nearby',
                'trigger_type': 'social_event',
                'conditions': {
                    'friend_device_connected': True
                },
                'priority': 6,
                'cooldown_hours': 48
            },
            {
                'name': 'Goal Progress Check',
                'description': 'Trigger weekly goal progress review',
                'trigger_type': 'goal_progress',
                'conditions': {
                    'check_frequency': 'weekly',
                    'has_active_goals': True
                },
                'priority': 5,
                'cooldown_hours': 168  # 1 week
            },
            {
                'name': 'App Jealousy',
                'description': 'Trigger when one app feels neglected',
                'trigger_type': 'pattern_detected',
                'conditions': {
                    'app_usage_drop_percentage': 50,
                    'comparison_days': 7
                },
                'priority': 4,
                'cooldown_hours': 72
            },
            {
                'name': 'Weekend Behavior Change',
                'description': 'Trigger when weekend usage differs significantly',
                'trigger_type': 'pattern_detected',
                'conditions': {
                    'is_weekend': True,
                    'usage_change_percentage': 30
                },
                'priority': 5,
                'cooldown_hours': 168
            },
            {
                'name': 'Morning Routine',
                'description': 'Trigger based on morning phone usage pattern',
                'trigger_type': 'time_based',
                'conditions': {
                    'time_range': {'start': '06:00', 'end': '09:00'},
                    'first_apps_checked': True
                },
                'priority': 6,
                'cooldown_hours': 24
            },
        ]
        
        created = []
        for data in triggers_data:
            trigger, created_flag = ConversationTrigger.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created_flag:
                created.append(trigger)
                self.stdout.write(f'  ✓ Created: {trigger.name}')
            else:
                self.stdout.write(f'  - Already exists: {trigger.name}')
        
        return created
