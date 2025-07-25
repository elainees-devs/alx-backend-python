from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Allows access to authenticated users who are participants in the conversation
    or are the sender of the message for unsafe methods.
    Allows access to any authenticated user for safe methods.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Check if user is authenticated
        if not user or not user.is_authenticated:
            return False

        # Allow all authenticated users to perform safe methods
        if request.method in SAFE_METHODS:
            return True

        # For unsafe methods (PUT, PATCH, DELETE), check if user is sender or participant
        is_sender = getattr(obj, 'sender', None) == user

        if hasattr(obj, 'participants'):
            is_participant = user in obj.participants.all()
        elif hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            is_participant = user in obj.conversation.participants.all()
        else:
            is_participant = False

        return is_sender or is_participant
