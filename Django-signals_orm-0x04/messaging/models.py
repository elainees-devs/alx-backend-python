from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessageManager

  
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False) # Indicates if the message has been edited

    # Self-referential FK for threaded replies
    parent_message = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True, blank=True)

    # Manager for unread messages
    objects = models.Manager()  # Default manager
    unread = UnreadMessageManager()  # Custom manager for unread messages

    def get_all_replies(self):
        """
        Recursively fetch all replies for this message.
        """
        all_replies = []

        def fetch_replies(message):
            for reply in message.replies.all():
                all_replies.append(reply)
                fetch_replies(reply)

        fetch_replies(self)
        return all_replies


    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}'
    
class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username} - Message ID {self.message.id}'
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history')
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, related_name='edited_messages', on_delete=models.CASCADE, null=True, blank=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'History for Message ID {self.message.id} edited by {self.edited_by} at {self.edited_at}'


