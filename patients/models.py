from django.db import models
from django.contrib.auth.models import User
from doctor.models import Schedule

# Create your models here.
class Appointment(models.Model):
    status_choices = (
        ('B', 'Booked'),
        ('F', 'Finished'),
        ('C', 'Canceled'),
        ('S', 'Started')
    )
    
    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    schedule = models.ForeignKey(Schedule, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=status_choices, default='B')
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.patient.username


class Document(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=30)
    document = models.FileField(upload_to='documents')

    def __str__(self):
        return self.title