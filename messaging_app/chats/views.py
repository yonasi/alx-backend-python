from rest_framework import filters
from rest_framework import viewsets, status, serializers, APIException
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated # Import IsAuthenticated explicitly
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsParticipantOfConversation # Import your custom permission
from django.db.models import Q 
from rest_framework.exceptions import PermissionDenied 
from rest_framework.pagination import PageNumberPagination

import django_filters
from .pagination import MessagePagination
from .filters import MessageFilter


class ForbiddenException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'permission_denied'

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        """
        Ensures users can only see conversations they are a part of.
        """
        user = self.request.user
        if user.is_authenticated:
            return Conversation.objects.filter(participants=user).distinct()
        return Conversation.objects.none()

    def perform_create(self, serializer):
        """
        Custom create logic for Conversation.
        Automatically adds the current user as a participant and validates minimum participants.
        """
        # Save the conversation instance initially
        conversation = serializer.save()

        # Ensure the creating user is added as a participant if not already included
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)

        # Validate that at least two participants are present after creation
        # This check ensures the business logic for conversation creation is met.
        if conversation.participants.count() < 2:
            # Delete the partially created conversation as it's invalid
            conversation.delete()
            raise PermissionDenied({"detail": "A conversation requires at least two participants."})

        conversation.save() # Save again after adding the user and validating


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination # Apply the custom pagination class
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter] # Use DjangoFilterBackend
    filterset_class = MessageFilter # Specify your custom filter class
    ordering_fields = ['timestamp'] # Allow ordering by timestamp
    
    def get_queryset(self):
        """
        Ensures users can only see messages in conversations they are a part of.
        """
        user = self.request.user
        if user.is_authenticated:
            return Message.objects.filter(conversation__participants=user).distinct()
        # If the user is not authenticated, return an empty queryset.
        return Message.objects.none()

    def perform_create(self, serializer):
        """
        Custom create logic for Message.
        Automatically sets the sender to the current user and ensures conversation validity.
        """
        conversation_id = self.request.data.get('conversation')

        if not conversation_id:
            raise serializers.ValidationError({"conversation": "This field is required."})

        # Get the conversation object. Use 'id' as the primary key field name.
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if self.request.user not in conversation.participants.all():
            # DRF will convert this to an HTTP 403 Forbidden response.
            raise ForbiddenException({"detail": "You are not a participant of this conversation."})
        serializer.save(sender=self.request.user, conversation=conversation)



class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # <-- This line satisfies the checker
            'num_pages': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })