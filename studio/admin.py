from django.contrib import admin
from .models import UserMessages


@admin.register(UserMessages)
class UserMessagesAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date', 'status_read')
    list_editable = ('status_read',)
