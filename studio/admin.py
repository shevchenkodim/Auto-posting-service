from django.contrib import admin
from .models import UserMessages
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class UserMessagesAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    short_text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = UserMessages
        fields = '__all__'

@admin.register(UserMessages)
class UserMessagesAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'date', 'status_read')
    list_editable = ('status_read',)
    form = UserMessagesAdminForm
