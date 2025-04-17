from django.db import models
from devices.models import Device

# Create your models here.


class Walk(models.Model):
    """
    Model representing a walk.
    """
    # user = models.ForeignKey(
    #     'auth.User', related_name='walks', on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, related_name='walks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='started', choices=[
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    def get_duration(self):
        """
        Calculate the duration of the walk.
        """
        if not self.end_time:
            return 0
        return self.end_time - self.start_time

    def add_event(self, event_type):
        """
        Add an event to the walk.
        """
        event = WalkEvent.objects.create(
            walk=self,
            event_type=event_type,
        )
        return event

    def __str__(self):
        return self.start_time.strftime("%Y-%m-%d %H:%M:%S")


class WalkEvent(models.Model):
    """
    Model representing an event during a walk.
    """
    walk = models.ForeignKey(
        Walk, related_name='events', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50, choices=[
        ('pee', 'Pee'),
        ('poo', 'Poo'),
        ('both', 'Both'),
        ('play', 'Play'),
        ('other', 'Other'),
    ])

    def __str__(self):
        return f"{self.event_type} at {self.walk.start_time}"
