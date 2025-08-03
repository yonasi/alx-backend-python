from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessageEditHistoryTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Original Message')

    def test_message_edit_creates_history(self):
        self.message.content = 'Edited Message'
        self.message.save()

        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, 'Original Message')
        self.assertTrue(self.message.edited)

    def test_no_history_on_create(self):
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 0)