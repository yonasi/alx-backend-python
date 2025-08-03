from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from messaging.models import Message
from django.contrib.auth.models import User

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
