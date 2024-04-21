from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

def is_doctor(user):
    return DoctorInfo.objects.filter(user=user).exists()

class Specialities(models.Model):
    specialities = models.CharField(max_length=100) # varible 
    icon = models.ImageField(upload_to="icons", null=True, blank=True)

    def __str__(self):
        return self.specialities


class DoctorInfo(models.Model):
    registration_number = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    postcode = models.CharField(max_length=15)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    photo_id = models.ImageField(upload_to="photo_id")
    doctor_credentials = models.ImageField(upload_to='doctor_credentials')
    profile_photo = models.ImageField(upload_to="profile_photo")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    description = models.TextField(null=True, blank=True)
    speciality = models.ForeignKey(Specialities, on_delete=models.DO_NOTHING, null=True, blank=True)
    price = models.FloatField(default=100)

    def __str__(self):
        return self.user.username
    
    @property
    def next_date(self):
        next_date = Schedule.objects.filter(user=self.user).filter(date__gt=datetime.now()).filter(booked=False).order_by('date').first()
        
        return next_date


class Schedule(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)