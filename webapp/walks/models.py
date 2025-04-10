from django.db import models

# Create your models here.


class Walk(models.Model):
    """
    Model representing a walk.
    """
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(
    #     'auth.User', related_name='walks', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.start_time.strftime("%Y-%m-%d %H:%M:%S")

    def get_duration(self):
        """
        Calculate the duration of the walk.
        """
        return self.end_time - self.start_time


class WalkEvent(models.Model):
    """
    Model representing an event during a walk.
    """
    walk = models.ForeignKey(
        Walk, related_name='events', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50, choices=[
        ('pee', 'Pee'),
        ('poo', 'Poo'),
        ('diarrhea', 'Diarrhea'),
        ('vomit', 'Vomit'),
        ('other', 'Other'),
    ])

    def __str__(self):
        return f"{self.event_type} at {self.walk.start_time}"
