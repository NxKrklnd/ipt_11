"""chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from chat import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.home, name='home'),  # Home route that redirects based on auth status
    path('chat/', views.chat_view, name='chat'),  # Actual chat view
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/login/', views.user_login, name='api-login'),
    path('api/logout/', views.user_logout, name='api-logout'),
    path('api/chat/', views.ChatHistoryList.as_view(), name='chat-history'),
    path('api/profile/', views.profile, name='user-profile'),
    # Django auth URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
