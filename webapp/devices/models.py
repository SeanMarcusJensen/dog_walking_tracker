from django.db import models

# Create your models here.

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.GenericIPAddressField()
    name = models.CharField(max_length=100)
    server_port = models.IntegerField()
    type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    
    def get_stream_url(self):
        return f"http://{self.ip}:{self.server_port}/stream"

    def __str__(self):
        return self.device_name