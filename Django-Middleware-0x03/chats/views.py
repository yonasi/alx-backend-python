from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages__sender')
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expected input: {'participants': [user_id1, user_id2, ...]}
        """
        participant_ids = request.data.get('participants', [])
        if not participant_ids or not isinstance(participant_ids, list):
            return Response({'error': 'Participants list is required.'}, status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response({'error': 'Some participant IDs are invalid.'}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('sender', 'conversation').all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Expected input: {'conversation_id': <UUID>, 'message_body': <TEXT>}
        Sender is derived from request.user
        """
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response({'error': 'conversation_id and message_body are required.'}, status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

    
        sender = request.user

        if sender not in conversation.participants.all():
            return Response({'error': 'You are not a participant of this conversation.'}, status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)