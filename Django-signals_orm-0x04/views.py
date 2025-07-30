from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    """
    Logs out the user, deletes the user account and redirects to the home page.
    """
    user = request.user
    logout(request)
    user.delete() #delete the user account after logout
    return redirect('home')