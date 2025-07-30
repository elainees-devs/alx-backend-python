from django.contrib import admin
from .models import Message, MessageHistory

admin.site.register(Message)
admin.site.register(MessageHistory)
admin.site.site_header = "Messaging Admin"
admin.site.site_title = "Messaging Admin Portal"
admin.site.index_title = "Welcome to the Messaging Admin Portal"
