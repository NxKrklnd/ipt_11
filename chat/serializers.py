from rest_framework import serializers
from .models import UserProfile, ChatHistory

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'role', 'bio']
        extra_kwargs = {'password': {'write_only': True}}

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['id', 'timestamp', 'user_message', 'bot_response']
        read_only_fields = ['id', 'timestamp']

    def validate_bot_response(self, value):
        """
        Validate that the bot response is not empty
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Bot response cannot be empty")
        return value.strip()