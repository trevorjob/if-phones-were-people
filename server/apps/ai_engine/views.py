from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import date, timedelta
from .tasks import generate_conversation_on_demand, generate_device_journal_entry, generate_app_journal_entry
from apps.devices.models import Device
from apps.applications.models import DeviceApp


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_conversations_for_user(request):
    """
    Manually trigger conversation generation for the authenticated user
    """
    user = request.user
    
    try:
        # Get yesterday's date for generating conversations
        target_date = date.today() - timedelta(days=1)
        
        # Trigger conversation generation task
        result = generate_conversation_on_demand(user.id)
        
        return Response({
            'message': 'Conversation generation triggered successfully',
            'user': user.username,
            'date': str(target_date)
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': str(e),
            'detail': 'Failed to generate conversations. Make sure you have usage data and OpenAI API key configured.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_journals_for_user(request):
    """
    Manually trigger journal generation for the authenticated user's devices and apps
    """
    user = request.user
    
    try:
        # Get yesterday's date for generating journals
        target_date = date.today() - timedelta(days=1)
        
        # Get user's active devices
        devices = Device.objects.filter(user=user, is_active=True)
        
        device_count = 0
        app_count = 0
        
        # Generate device journals
        for device in devices:
            print(f"started generating journal for device")
            try:
                generate_device_journal_entry(device, target_date)
                device_count += 1
            except Exception as e:
                print(f"Error generating journal for device {device.id}: {str(e)}")
        
        # Generate app journals for top apps
        top_apps = DeviceApp.objects.filter(
            device__user=user,
            device__is_active=True
        ).select_related('app', 'device')[:10]  # Top 10 apps
        
        for device_app in top_apps:
            try:
                generate_app_journal_entry(device_app, target_date)
                app_count += 1
            except Exception as e:
                print(f"Error generating journal for app {device_app.id}: {str(e)}")
        
        return Response({
            'message': 'Journal generation triggered successfully',
            'device_journals_generated': device_count,
            'app_journals_generated': app_count,
            'date': str(target_date)
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'error': str(e),
            'detail': 'Failed to generate journals. Make sure you have usage data and OpenAI API key configured.'
        }, status=status.HTTP_400_BAD_REQUEST)
