from django.db import models

class UnreadMessageManager(models.Manager):
   def unread_for_user(self, user):
       return self.get_queryset().filter(
           receiver=user,
           read=False
       ).only('id', 'sender', 'content', 'timestamp')
