from django.contrib import admin
from .models.messages import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "user_name", "email", )
    # list_filter = ("created", "author")