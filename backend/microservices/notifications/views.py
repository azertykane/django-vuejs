# notifications/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Notification
from .serializers import NotificationSerializer

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_notification(request):
    data = {
        'destinataire': request.data['destinataire'],
        'titre': request.data['titre'],
        'message': request.data['message'],
        'type': request.data.get('type', 'info'),
    }
    serializer = NotificationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
