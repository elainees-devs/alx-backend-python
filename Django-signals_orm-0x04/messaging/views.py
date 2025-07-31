from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message  # Ensure your Message model is imported

@login_required
def delete_user(request):
    """
    Logs out the user, efficiently fetches their messages and threaded replies
    using select_related and prefetch_related, deletes the user account,
    and redirects to the home page.
    """
    user = request.user

    # Optimize message query to minimize DB hits before deletion
    messages = Message.objects.filter(sender=user, parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(
            'replies',                    # Direct replies
            'replies__sender',            # Sender of direct replies
            'replies__receiver',          # Receiver of direct replies
            'replies__replies',           # Replies to replies
            'replies__replies__sender',   # Sender of replies to replies
            'replies__replies__receiver'  # Receiver of replies to replies
        )

    # (Optional) You could log, archive, or process messages before deletion

    logout(request)
    user.delete()  # Triggers cleanup via post_delete signal
    return redirect('home')
