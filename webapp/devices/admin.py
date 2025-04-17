from django.contrib import admin
from .models import Device, DoorFrame

# Register your models here.
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip', 'server_port', 'type', 'location', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'ip')
    list_filter = ('type', 'status')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

@admin.register(DoorFrame)
class DoorFrameAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'x', 'y', 'width', 'height', 'created_at', 'updated_at')
    search_fields = ('device__name',)
    list_filter = ('device__type',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'