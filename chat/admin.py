from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, ChatHistory

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'bio', 'theme_preference')}),
        ('Settings', {'fields': ('notification_enabled',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'user_message', 'is_flagged')
    list_filter = ('timestamp', 'is_flagged', 'user')
    search_fields = ('user__username', 'user_message', 'bot_response')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(ChatHistory, ChatHistoryAdmin)
