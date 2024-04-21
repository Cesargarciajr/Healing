from django.shortcuts import render, redirect
from doctor.models import Specialities, DoctorInfo, is_doctor, Schedule
from patients.models import Appointment, Document
from django.contrib.messages import constants
from django.contrib import messages
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required

@login_required
def doctor_registration(request):

    if is_doctor(request.user):
        messages.add_message(request, constants.WARNING, "You're already a Doctor!")
        return redirect('/doctors/schedule')

    if request.method == "GET":
        specialities = Specialities.objects.all()
        return render(request, 'doctor_registration.html', {'specialities': specialities}) # {'table': variable}
    elif request.method == "POST": #getting all the data from the inputs in the view "variable = request.POST.get('name_of_the_input')"
        registration_number = request.POST.get('registration_number')
        name = request.POST.get('name')
        postcode = request.POST.get('postcode')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        photo_id = request.FILES.get('photo_id')
        doctor_credentials = request.FILES.get('doctor_credentials')
        profile_photo = request.FILES.get('profile_photo')
        speciality = request.POST.get('speciality')
        description = request.POST.get('description')
        price = request.POST.get('price')

        #TODO: Validations 

        doctor_data = DoctorInfo(
            # model.name = variable.name
            registration_number=registration_number,
            name=name,
            postcode=postcode,
            address1=address1,
            address2=address2,
            photo_id=photo_id,
            doctor_credentials=doctor_credentials,
            profile_photo=profile_photo,
            user=request.user,
            description=description,
            speciality_id=speciality,
            price=price,
        )
        doctor_data.save()

        messages.add_message(request, constants.SUCCESS, 'Doctor registration completed successfully!')

        return redirect('/doctors/schedule')
    
def schedule(request):

    if not is_doctor(request.user):
        messages.add_message(request, constants.WARNING, 'Only Doctors can access this page!')
        return redirect('/users/logout')
    
    if request.method == "GET":
        doctor_info = DoctorInfo.objects.get(user=request.user)
        schedule = Schedule.objects.filter(user=request.user)
        return render(request, 'schedule.html', {'doctor_info': doctor_info, 'schedule': schedule, 'is_doctor': is_doctor(request.user),})
    elif request.method == "POST":
        date = request.POST.get('date')

        formated_date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
    
        if formated_date <= datetime.now():
            messages.add_message(request, constants.WARNING, 'Date selected invalid')
            return redirect('/doctors/schedule')
        
        open_schedule = Schedule(
            date=date,
            user=request.user
        )
        open_schedule.save()

        messages.add_message(request, constants.SUCCESS, 'Schedule updated successfully!')
        return redirect('/doctors/schedule')
    
def appointments_doctor(request):
    if not is_doctor(request.user):
        messages.add_message(request, constants.WARNING, 'Only Doctors can access this page.')
        return redirect('/users/logout')
    
    specialities_filter = request.GET.get('specialities')
    date_filter = request.GET.get('date')
    today = datetime.now().date()

    appointments_today = Appointment.objects.filter(schedule__user=request.user).filter(schedule__date__gte=today).filter(schedule__date__lt=today + timedelta(days=1))
    
    remaining_appointments= Appointment.objects.exclude(id__in=appointments_today.values('id')).filter(schedule__user=request.user)

    if specialities_filter:
        appointments_today = Appointment.objects.filter(schedule__user=request.user).filter(schedule__date__gte=today).filter(schedule__date__lt=today + timedelta(days=1)).filter(schedule__user__doctorinfo__speciality__specialities__icontains=specialities_filter)
        
        remaining_appointments= Appointment.objects.exclude(id__in=appointments_today.values('id')).filter(schedule__user__doctorinfo__speciality__specialities__icontains=specialities_filter)

    if date_filter:
        appointments_today = Appointment.objects.filter(schedule__user=request.user).filter(schedule__date__gte=today).filter(schedule__date__lt=today + timedelta(days=1)).filter(schedule__date__contains=date_filter)

        remaining_appointments= Appointment.objects.exclude(id__in=appointments_today.values('id')).filter(schedule__date__contains=date_filter)

    context = {
        'appointments_today': appointments_today,
        'remaining_appointments': remaining_appointments, 
        'is_doctor': is_doctor(request.user)
    }

    return render(request, 'appointments_doctor.html', context)


def access_appointment_doctor(request, id_appointment):
    if not is_doctor(request.user):
        messages.add_message(request, constants.WARNING, 'Only Doctors can access this page.')
        return redirect('/users/logout')
    

    if request.method == "GET":
        appointment = Appointment.objects.get(id=id_appointment)
        documents = Document.objects.filter(appointment=appointment)
        return render(request, 'access_appointment_doctor.html', {'appointment': appointment, 'documents': documents, 'is_doctor': is_doctor(request.user)})
    elif request.method == "POST":
        appointment = Appointment.objects.get(id=id_appointment)
        link = request.POST.get('link')

        if appointment.status == 'C':
            messages.add_message(request, constants.WARNING, 'The appointment was cancelled.')
            return redirect(f'/doctors/access_appointment_doctor/{id_appointment}')
        elif appointment.status == 'F':
            messages.add_message(request, constants.WARNING, 'The appointment is already finished.')
            return redirect(f'/doctors/access_appointment_doctor/{id_appointment}')
        
        appointment.link = link
        appointment.status = 'S'
        appointment.save()

        messages.add_message(request, constants.SUCCESS, 'Appointment is finished')
        return redirect(f'/doctors/access_appointment_doctor/{id_appointment}')
    

def finish_appointment(request, id_appointment):
    if not is_doctor(request.user):
        messages.add_message(request, constants.WARNING, 'Only Doctors can access this page.')
        return redirect('/users/logout')
        
    appointment = Appointment.objects.get(id=id_appointment)
    if request.user != appointment.schedule.user:
        messages.add_message(request, constants.ERROR, 'This appointment does not belongs to you.')
        return redirect(f'/doctors/access_appointment_doctor/{id_appointment}')
    
    appointment.status = 'F'
    appointment.save()
    return redirect(f'/doctors/access_appointment_doctor/{id_appointment}')


def add_document(request, id_appointment):
    if not is_doctor(request.user):
        messages.add_message(request, constants.WARNING, 'Only Doctors can access this page.')
        return redirect('/users/logout')
    
    appointment = Appointment.objects.get(id=id_appointment)
    if request.user != appointment.schedule.user:
        messages.add_message(request, constants.ERROR, 'This appointment does not belongs to you.')
        return redirect(f'/doctors/schedule/')
    
    title = request.POST.get('title')
    document = request.FILES.get('document')

    if not document:
        messages.add_message(request, constants.WARNING, 'Please add document.')
        return redirect(f'/doctors/access_appointment_doctor/{id_appointment}')
    
    document = Document(
        appointment=appointment,
        title=title,
        document=document
    )
    document.save()

    messages.add_message(request, constants.SUCCESS, 'Document added successfully!')
    return redirect(f'/doctors/access_appointment_doctor/{id_appointment}')