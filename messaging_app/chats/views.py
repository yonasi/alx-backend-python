# messaging_app/chats/views.py

from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message, User 
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsParticipantOfConversation 
from rest_framework import serializers
from django.db.models import Q

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        """
        Ensures users can only see conversations they are a part of.
        """
        user = self.request.user
        if user.is_authenticated:
            # Filter conversations where the current user is a participant
            return Conversation.objects.filter(participants=user).distinct()
        # If the user is not authenticated, return an empty queryset
        return Conversation.objects.none()

    def perform_create(self, serializer):
        """
        Custom create logic for Conversation.
        Automatically adds the current user as a participant.
        """
        # Save the conversation instance initially
        conversation = serializer.save()

        # Ensure the creating user is added as a participant if not already included
        # The serializer might already handle adding participants via participant_ids
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)

        # Validate that at least two participants are present after creation
        if conversation.participants.count() < 2:
            # Delete the partially created conversation if it doesn't meet the minimum participant requirement
            conversation.delete()
            raise serializers.ValidationError({"error": "At least two participants are required for a conversation."})

        conversation.save() # Save again after adding the user

    # The default `create` method from ModelViewSet will call `perform_create`
    # You generally don't need to override `create` directly unless you have very specific
    # response formatting or pre-validation that can't be handled by `perform_create` or serializers.
    # The original `create` method's participant validation is now handled in `perform_create`
    # and via serializer validation (if you add it to the serializer).
    # For simplicity and DRF best practices, it's better to let `perform_create` handle this.
    # If you still want the exact error message from your original `create` method:
    # def create(self, request, *args, **kwargs):
    #     participant_ids = request.data.get('participant_ids', []) # Assuming serializer uses 'participant_ids'
    #     if not participant_ids or len(participant_ids) < 1: # Check for at least 1 participant from request
    #         return Response(
    #             {"error": "At least one participant (besides yourself) is required to start a conversation."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     # Let the default ModelViewSet.create handle the rest, which calls perform_create
    #     return super().create(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    # Apply your custom permission class
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        """
        Ensures users can only see messages in conversations they are a part of.
        """
        user = self.request.user
        if user.is_authenticated:
            # Filter messages where the current user is a participant in the associated conversation
            return Message.objects.filter(conversation__participants=user).distinct()
        # If the user is not authenticated, return an empty queryset
        return Message.objects.none()

    def perform_create(self, serializer):
        """
        Custom create logic for Message.
        Automatically sets the sender to the current user and ensures conversation validity.
        """
        conversation_id = self.request.data.get('conversation')

        if not conversation_id:
            raise serializers.ValidationError({"conversation": "This field is required."})

        conversation = get_object_or_404(Conversation, id=conversation_id) # Use 'id' for primary key

        if self.request.user not in conversation.participants.all():
            raise serializers.ValidationError(
                {"error": "You are not a participant of this conversation."}
            )

        # Set the sender to the current authenticated user
        serializer.save(sender=self.request.user, conversation=conversation)
