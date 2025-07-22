from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to authenticated users who are participants in the conversation
    or are the sender of the message.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Check if user is authenticated
        if not user or not user.is_authenticated:
            return False

        # Allow if user is sender
        is_sender = getattr(obj, 'sender', None) == user

        # Check if user is participant
        if hasattr(obj, 'participants'):
            is_participant = user in obj.participants.all()
        elif hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            is_participant = user in obj.conversation.participants.all()
        else:
            is_participant = False

        return is_sender or is_participant
