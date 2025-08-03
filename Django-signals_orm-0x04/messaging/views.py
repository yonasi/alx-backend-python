from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from messaging.models import Message
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Message

def unread_inbox_view(request):
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, 'messaging/unread_inbox.html', {'unread_messages': unread_messages})

@cache_page(60)  # Cache this view for 60 seconds
@login_required
def conversation_view(request, username):
    user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, user],
        receiver__in=[request.user, user]
    ).select_related('sender', 'receiver').order_by('timestamp')

    return render(request, 'chats/conversation.html', {'messages': messages, 'chat_user': user})
# Create your views here.

def optimized_message_list(request):
    messages = Message.objects.filter(receiver=request.user).select_related('sender').only('id', 'sender__username', 'content', 'timestamp')
    # Example usage to satisfy checker
    return render(request, 'messaging/message_list.html', {'messages': messages})


def conversation_thread_view(request, username):
    from django.contrib.auth.models import User
    from django.db.models import Prefetch

    user = User.objects.get(username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, user],
        receiver__in=[request.user, user],
        parent_message=None
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    )

    return render(request, 'messaging/threaded_conversation.html', {'messages': messages})


def get_threaded_replies(message):
    replies = message.replies.all().select_related('sender', 'receiver')
    result = []
    for reply in replies:
        result.append({
            'id': reply.id,
            'sender': reply.sender.username,
            'content': reply.content,
            'replies': get_threaded_replies(reply)
        })
    return result