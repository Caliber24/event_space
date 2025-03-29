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
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    
    def __str__(self):
        return f"{self.title} - {self.creator.email}"
