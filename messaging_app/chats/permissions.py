from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow access to objects owned by the requesting user.
    """

    def has_object_permission(self, request, view, obj):
        """
        Allow access if the user is the sender or a participant in the related conversation.
        """

        # Check if the request user is the sender
        is_sender = getattr(obj, 'sender', None) == request.user

        # Check if the object has direct participants (e.g. Conversation)
        if hasattr(obj, 'participants'):
            is_participant = request.user in obj.participants.all()
        # Check if the object has a conversation with participants (e.g. Message)
        elif hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            is_participant = request.user in obj.conversation.participants.all()
        else:
            is_participant = False

        return is_sender or is_participant
