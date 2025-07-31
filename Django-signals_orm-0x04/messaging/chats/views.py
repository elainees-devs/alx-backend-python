from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from models import Message, Conversation

@cache_page(60)
def conversation_messages(request, conversation_id):
    """
    Display a list of messages in a conversation.
    The view is cached for 60 seconds to reduce DB hits.
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).order_by('-timestamp')
    return render(request, 'chats/conversation_messages.html', {
        'conversation': conversation,
        'messages': messages
    })
