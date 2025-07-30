from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=f'New message from {instance.sender.username}: {instance.content}'
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            original_message = Message.objects.get(pk=instance.pk)
            if original_message.content != instance.content:
                MessageHistory.objects.create(
                    message=original_message,
                    old_content=original_message.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            instance.edited = False

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete all messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(reciever=instance).delete()

    # Delete all notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Delete all message histories edited by the user
    MessageHistory.objects.filter(edited_by=instance).delete()
