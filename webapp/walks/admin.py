from django.contrib import admin
from .models import Walk, WalkEvent

# Register your models here.


@admin.register(Walk)
class WalkAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'status')
    search_fields = ('id', 'start_time', 'end_time', 'status')
    list_filter = ('status',)
    ordering = ('-start_time',)
    date_hierarchy = 'start_time'
    list_per_page = 20


@admin.register(WalkEvent)
class WalkEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'walk', 'event_type')
    search_fields = ('id', 'walk__id', 'event_type')
    list_filter = ('event_type',)
    ordering = ('-walk__start_time',)
    list_per_page = 20
