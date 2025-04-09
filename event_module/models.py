from django.conf import settings
from django.db import models
# Create your models here.


class Event(models.Model):
    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'COMPLETED'),
        (2, 'CANCELLED'),
        
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.IntegerField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='events', blank=True)
    
    
    def __str__(self):
        return f"{self.title} - {self.creator.email}"