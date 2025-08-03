from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        original = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if original.content != instance.content:
        MessageHistory.objects.create(message=instance, old_content=original.content)
        instance.edited = True

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for user
    Notification.objects.filter(user=instance).delete()

    # MessageHistory will be auto-deleted because of CASCADE on Message foreign key