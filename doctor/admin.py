from django.contrib import admin
from .models import Specialities, DoctorInfo, Schedule

# Register your models here.
admin.site.register(Specialities)
admin.site.register(DoctorInfo)
admin.site.register(Schedule)