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
    
    def get_registration_url(self):
        return f"http://{self.ip}:{self.server_port}/register"

    def get_stream_url(self):
        return f"http://{self.ip}:{self.server_port}/stream"
    
    def get_websocket_url(self):
        return f"ws://{self.ip}:{self.server_port}/stream/ws"
    
    def get_door_frame(self):
        return DoorFrame.objects.filter(device=self).first()
    
    def update_door_frame(self, x, y, width, height):
        door_frame, created = DoorFrame.objects.get_or_create(device=self, defaults={
            'x': x,
            'y': y,
            'width': width,
            'height': height,
        })
        if not created:
            # Update existing door frame
            door_frame.x = x
            door_frame.y = y
            door_frame.width = width
            door_frame.height = height
        door_frame.save()

    def __str__(self):
        return self.name

class DoorFrame(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{id}({self.device.name})"