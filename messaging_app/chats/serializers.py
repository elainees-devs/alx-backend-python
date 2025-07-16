from rest_framework import serializers
from .models import User, Conversation, Message
from django.utils.timesince import timesince
from rest_framework.exceptions import ValidationError

# ------------------------
# User Serializer
# ------------------------

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

# ------------------------
# Message Serializer
# ------------------------

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source='sender.email', read_only=True)
    time_since_sent = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender_email', 'message_body', 'sent_at', 'time_since_sent']

    def get_time_since_sent(self, obj):
        return timesince(obj.sent_at)

# ------------------------
# Conversation Serializer (with nested messages)
# ------------------------

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'updated_at', 'messages']

    def validate(self, data):
        if not data.get('participants'):
            raise ValidationError("A conversation must have at least one participant.")
        return data
