from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from models import Conversation, Message
from serializers import ConversationSerializer, MessageSerializer
from permissions import IsParticipantOfConversation
from pagination import MessagePagination
from filters import MessageFilters

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['timestamp']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        return super().perform_create(serializer)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filter_class = MessageFilters

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        conversation_id = conversation.id if conversation else None

        if self.request.user not in conversation.participants.all():
            detail = {
                "error": "You are not a participant in this conversation.",
                "conversation_id": conversation_id
            }
            # Return Response with 403 FORBIDDEN status
            return Response(detail, status=status.HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user)
