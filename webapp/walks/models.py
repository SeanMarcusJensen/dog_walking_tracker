from django.db import models

# Create your models here.


class Walk(models.Model):
    """
    Model representing a walk.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    duration = models.DurationField()
    distance = models.FloatField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
