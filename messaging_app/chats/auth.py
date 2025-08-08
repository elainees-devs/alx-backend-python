# Importing views for obtaining and refreshing JWT tokens from the Simple JWT package
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # View that returns access and refresh tokens when given valid user credentials
    TokenRefreshView,     # View that returns a new access token when given a valid refresh token
)

# Importing Django's path function to define URL patterns
from django.urls import path

# Defining URL patterns for the JWT authentication endpoints
urlpatterns = [
    # Endpoint to obtain a pair of tokens (access and refresh) after login
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    
    # Endpoint to refresh the access token using the refresh token
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
