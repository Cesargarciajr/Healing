from django.shortcuts import render, redirect
from doctor.models import DoctorInfo, Specialities, Schedule, is_doctor
from datetime import datetime
from .models import Appointment, Document
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
def home(request):
    if request.method == "GET":
        doctor_filter = request.GET.get('doctor')
        specialities_filter = request.GET.getlist('specialities') # get a list of filters
        doctors = DoctorInfo.objects.all()
        specialities = Specialities.objects.all()
        if doctor_filter:
            doctors = doctors.filter(name__icontains = doctor_filter)
        
        if specialities_filter:
            doctors = doctors.filter(speciality_id__in = specialities_filter) # get all selected specialities
        return render(request, 'home.html', {'doctors':doctors, 'specialities': specialities, 'is_doctor': is_doctor(request.user),})

   
def booking(request, id_doctors_data):
    if request.method == "GET":
        doctor = DoctorInfo.objects.get(id=id_doctors_data)
        schedule = Schedule.objects.filter(user=doctor.user).filter(date__gte=datetime.now()).filter(booked=False)
        return render(request, 'booking.html', {'doctor': doctor, 'schedule': schedule, 'is_doctor': is_doctor(request.user),})
    

def appointment(request, id_schedule):
    if request.method == "GET":
        schedule = Schedule.objects.get(id=id_schedule)

        appointment = Appointment(
            patient=request.user,
            schedule=schedule
        )

        appointment.save()
        # TODO: Sugestão Tornar atomico
        schedule.booked = True
        schedule.save()

        messages.add_message(request, constants.SUCCESS, 'Appointment booked sucessfully!')

        return redirect('/patients/my_bookings/')


def my_bookings(request):
    if request.method == "GET":
        #TODO: desenvolver filtros
        my_bookings = Appointment.objects.filter(patient=request.user).filter(schedule__date__gte=datetime.now())

        specialities_filter = request.GET.get('specialities')
        date_filter = request.GET.get('date')
        
        if specialities_filter:
            my_bookings = my_bookings.filter(schedule__user__doctorinfo__speciality__specialities__icontains=specialities_filter)

        if date_filter:
            my_bookings = my_bookings.filter(schedule__date__contains=date_filter)

        return render(request, 'my_bookings.html', {'my_bookings': my_bookings, 'is_doctor': is_doctor(request.user),})


def access_appointment(request, id_appointment):
    if request.method == 'GET':
        appointment = Appointment.objects.get(id=id_appointment)
        doctor_info = DoctorInfo.objects.get(user=appointment.schedule.user)
        documents = Document.objects.filter(appointment=appointment)
        return render(request, 'access_appointment.html', {'appointment': appointment, 'doctor_info': doctor_info, 'documents': documents, 'is_doctor': is_doctor(request.user)})
