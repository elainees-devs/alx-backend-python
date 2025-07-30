from django.db.models import signals
from django.dispatch import receiver
from .models import Message, Notification

@receiver(signals.post_save, sender=Message)   
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=f'New message from {instance.sender.username}: {instance.content}'
        )