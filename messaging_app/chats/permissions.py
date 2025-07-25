from rest_framework import permissions

class IsMessageOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow owners of a message or participants of a conversation
    to view/edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user if they are the sender
        # or a participant in the conversation.
        if request.method in permissions.SAFE_METHODS:
            # Check if the user is the sender of the message
            if hasattr(obj, 'sender') and obj.sender == request.user:
                return True
            # Check if the user is a participant in the conversation associated with the message
            if hasattr(obj, 'conversation') and request.user in obj.conversation.participants.all():
                return True
            # If the object itself is a Conversation, check if the user is a participant
            if hasattr(obj, 'participants') and request.user in obj.participants.all():
                return True
            return False
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if hasattr(obj, 'sender') and obj.sender == request.user:
                return True
            if hasattr(obj, 'participants') and request.user in obj.participants.all():
                return True
            return False
        return False

class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to view/edit it.
    Assumes the model instance (e.g., Conversation) has a 'participants' ManyToManyField.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Ensure the object has a 'participants' attribute (e.g., a Conversation instance)
        if hasattr(obj, 'participants'):
            # Check if the requesting user is one of the participants in the conversation
            return request.user in obj.participants.all()
        return False