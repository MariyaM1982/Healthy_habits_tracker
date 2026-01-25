from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.action == 'list':
            return Habit.objects.filter(user=self.request.user)
        return Habit.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
@api_view(['POST'])
def set_telegram_chat_id(request):
    chat_id = request.data.get('chat_id')
    if chat_id:
        request.user.telegram_chat_id = chat_id
        request.user.save()
        return Response({'status': 'ok'})
    return Response({'status': 'error', 'message': 'chat_id required'}, status=400)