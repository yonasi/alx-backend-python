from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager

class Message(models.Model):
    ...
    read = models.BooleanField(default=False)
    objects = models.Manager()  # Default Manager
    unread = UnreadMessagesManager()  # Custom Manager (called 'unread')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey('messaging.Message', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    read = models.BooleanField(default=False)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey('messaging.Message', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class MessageHistory(models.Model):
    message = models.ForeignKey('messaging.Message', on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)