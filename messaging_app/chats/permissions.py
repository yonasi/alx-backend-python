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
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Ensure the object has a 'participants' 
        if hasattr(obj, 'participants'):
            # Check if the requesting user is one of the participants in the conversation
            return request.user in obj.participants.all()
        return False
    
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
     """
    Custom permission to allow only authenticated users to access the API,
    and only participants of a conversation to view, send, update, or delete
    messages
    """
     
     def has_permission(self, request, view):
        """
        Global permission check for authenticated users.
        Allows access to the API if the user is authenticated.
        """
        # Allow only authenticated users to access the API
        return request.user and request.user.is_authenticated

     def has_object_permission(self, request, view, obj):
        """
        Object-level permission check.
        Allows access if the user is a participant in the relevant conversation.
        """
        # If the user is not authenticated, they shouldn't have object access (redundant due to has_permission, but good for clarity)
        if not request.user.is_authenticated:
            return False

        # check if the object is a Message or a Conversation and check participation
        if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            # check its conversation's participants
            return request.user in obj.conversation.participants.all()
        elif hasattr(obj, 'participants'):
            # check its participants directly
            return request.user in obj.participants.all()

        # If the object doesn't have a recognizable conversation or participants attribute, deny access
        return False