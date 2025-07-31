from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from .models import Message, Conversation 
from django.views.decorators.cache import cache_page


@login_required
def user_inbox(request):
    """
    Displays unread messages for the logged-in user.
    Uses .only() to optimize DB query to fetch only needed fields.
    """
    user = request.user

    # Efficiently get unread messages using custom manager
    unread_messages = Message.unread.unread_for_user(user).only('content', 'sender__username')


    # Example: log unread messages
    for msg in unread_messages:
        print(f"Unread: {msg.content} from {msg.sender.username}")

    return render(request, 'inbox.html', {'unread_messages': unread_messages})


@login_required
def delete_user(request):
    """
    Logs out the user, efficiently fetches their messages and threaded replies
    using select_related and prefetch_related, deletes the user account,
    and redirects to the home page.
    """
    sender = request.user

    # Optimize message query to minimize DB hits before deletion
    messages = Message.objects.filter(sender=sender, parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(
            'replies',                    # Direct replies
            'replies__sender',            # Sender of direct replies
            'replies__receiver',          # Receiver of direct replies
            'replies__replies',           # Replies to replies
            'replies__replies__sender',   # Sender of replies to replies
            'replies__replies__receiver'  # Receiver of replies to replies
        )

    # Optional: process or log messages before deletion
    for msg in messages:
        print(f"Message: {msg.content} - Replies: {msg.replies.count()}")

    logout(request)
    sender.delete()  # Triggers post_delete signal
    return redirect('home')

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
