from django.contrib import admin

# Register your models here.
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'video_size', 'extension', 'created_at')
    search_fields = ('id', 'extension')
    list_filter = ('extension',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
