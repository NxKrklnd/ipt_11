from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, throttle_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from .models import UserProfile, ChatHistory
from .serializers import ChatHistorySerializer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .groq_client import GroqClient
import re

# Initialize Groq client
groq_client = GroqClient()

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        email = request.POST.get('email', '').strip()
        
        # Validate input fields
        if not all([username, password, email]):
            messages.error(request, 'All fields are required')
            return redirect('register')

        # Username validation
        if len(username) < 3:
            messages.error(request, 'Username must be at least 3 characters long')
            return redirect('register')
        if not re.match(r'^[\w.@+-]+$', username):
            messages.error(request, 'Username can only contain letters, numbers, and @/./+/-/_ characters')
            return redirect('register')

        # Enhanced Password validation
        if len(password) < 12:  # Increased from 8 to 12
            messages.error(request, 'Password must be at least 12 characters long')
            return redirect('register')
        if not re.search(r'[A-Z]', password):
            messages.error(request, 'Password must contain at least one uppercase letter')
            return redirect('register')
        if not re.search(r'[a-z]', password):
            messages.error(request, 'Password must contain at least one lowercase letter')
            return redirect('register')
        if not re.search(r'[0-9]', password):
            messages.error(request, 'Password must contain at least one number')
            return redirect('register')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, 'Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)')
            return redirect('register')
        if re.search(username, password, re.IGNORECASE) or re.search(email.split('@')[0], password, re.IGNORECASE):
            messages.error(request, 'Password cannot contain your username or email')
            return redirect('register')

        # Email validation with additional checks
        try:
            validate_email(email)
            email_domain = email.split('@')[1]
            if email_domain in ['tempmail.com', 'throwaway.com']:  # Add more disposable email domains
                messages.error(request, 'Please use a valid email address. Temporary email services are not allowed.')
                return redirect('register')
        except ValidationError:
            messages.error(request, 'Please enter a valid email address')
            return redirect('register')

        # Check for existing username/email
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect('register')

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email or try logging in.')
            return redirect('register')

        try:
            user = UserProfile.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            # Set initial account settings
            user.notification_enabled = True
            user.theme_preference = 'system'
            user.save()
            
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to our platform.')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'An error occurred during registration: {str(e)}')
            return redirect('register')

    return render(request, 'registration/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not all([username, password]):
            messages.error(request, 'Both username and password are required')
            return render(request, 'registration/login.html')

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Your account is disabled')
            else:
                messages.error(request, 'Invalid username or password')
        except Exception as e:
            messages.error(request, 'An error occurred during login')

    return render(request, 'registration/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    if request.method == 'POST':
        try:
            user = request.user
            bio = request.POST.get('bio', '').strip()
            theme = request.POST.get('theme_preference', 'system')
            notifications = request.POST.get('notification_enabled') == 'on'

            user.bio = bio
            user.theme_preference = theme
            user.notification_enabled = notifications
            user.save()

            messages.success(request, 'Profile updated successfully')
        except Exception as e:
            messages.error(request, 'An error occurred while updating your profile')

    # Get theme choices from the model field
    theme_choices = UserProfile._meta.get_field('theme_preference').choices

    return render(request, 'profile.html', {
        'user': request.user,
        'theme_choices': theme_choices
    })

@login_required
def chat_view(request):
    """
    Main chat view that serves as the home page for authenticated users.
    Requires authentication - will redirect to login if user is not authenticated.
    """
    return render(request, 'chat.html')

def home(request):
    """
    Home view that redirects to chat if authenticated, otherwise to login.
    """
    if request.user.is_authenticated:
        return redirect('chat')
    return redirect('login')

class ChatRateThrottle(UserRateThrottle):
    rate = '10/minute'

class ChatHistoryList(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [ChatRateThrottle]

    def get(self, request):
        try:
            chats = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')[:50]  # Get last 50 messages
            serializer = ChatHistorySerializer(chats, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Failed to fetch chat history'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            # Enforce rate limiting
            self.check_throttles(request)
            
            # Validate message content
            user_message = request.data.get('user_message', '').strip()
            if not user_message:
                return Response(
                    {'error': 'Message cannot be empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get recent chat history for context
            recent_chats = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')[:5]
            
            # Get response from Groq
            bot_response = groq_client.get_response(user_message, recent_chats)

            # Create chat history entry
            chat_data = {
                'user_message': user_message,
                'bot_response': bot_response
            }

            serializer = ChatHistorySerializer(data=chat_data)
            if serializer.is_valid():
                chat_history = serializer.save(user=request.user)
                
                # Check for inappropriate content
                if self._contains_inappropriate_content(user_message):
                    chat_history.is_flagged = True
                    chat_history.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error in chat endpoint: {str(e)}")  # Add logging for debugging
            return Response(
                {'error': 'Failed to process message'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        """
        Delete all chat history for the current user
        """
        try:
            ChatHistory.objects.filter(user=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(f"Error deleting chat history: {str(e)}")
            return Response(
                {'error': 'Failed to clear chat history'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _contains_inappropriate_content(self, message):
        # Implement content filtering logic here
        inappropriate_words = ['spam', 'abuse', 'hate']
        return any(word in message.lower() for word in inappropriate_words)
