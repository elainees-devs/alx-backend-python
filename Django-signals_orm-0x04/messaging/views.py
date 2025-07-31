from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message  # Import your Message model

@login_required
def delete_user(request):
    """
    Logs out the user, fetches their messages and threaded replies for optional processing,
    deletes the user account, and redirects to the home page.
    """
    user = request.user

    # Optional: Fetch all top-level messages sent by the user with their threaded replies
    messages = Message.objects.filter(sender=user, parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(
            'replies',                   # direct replies
            'replies__sender',           # sender of replies
            'replies__receiver',         # receiver of replies
            'replies__replies',          # nested replies
            'replies__replies__sender',
            'replies__replies__receiver'
        )

    # (Optional) You can log them, export them, or do something before deleting the account
    # For example:
    # for msg in messages:
    #     print(f"{msg.content} with {msg.replies.count()} replies")

    logout(request)
    user.delete()  # Triggers post_delete signal for cleanup
    return redirect('home')
