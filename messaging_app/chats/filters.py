import django_filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model # To get the active user model

User = get_user_model() # Get the active user model, whether default or custom

class MessageFilter(django_filters.FilterSet):
    """
    Filter for Message objects.
    Allows filtering by:
    - `conversation_participant`
    - `start_date`: 
    - `end_date`: 
    """
    conversation_participant = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='conversation__participants', # Traverse to Conversation's participants
        to_field_name='id', # Filter by user ID
        help_text="Filter messages by a participant's user ID in the conversation.",
    )

    start_date = django_filters.DateFilter(
        field_name='timestamp',
        lookup_expr='gte', # Greater than or equal to
        help_text="Filter messages sent on or after this date (YYYY-MM-DD)."
    )
    end_date = django_filters.DateFilter(
        field_name='timestamp',
        lookup_expr='lte', # Less than or equal to
        help_text="Filter messages sent on or before this date (YYYY-MM-DD)."
    )

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'conversation_participant', 'start_date', 'end_date']
        