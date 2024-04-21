from django.urls import path
from . import views

urlpatterns = [
    path('doctor_registration/', views.doctor_registration, name="doctor_registration"),
    path('schedule/', views.schedule, name="schedule"),
    path('appointments_doctor/', views.appointments_doctor, name="appointments_doctor"),
    path('access_appointment_doctor/<int:id_appointment>/', views.access_appointment_doctor, name="access_appointment_doctor"),
    path('finish_appointment/<int:id_appointment>/', views.finish_appointment, name="finish_appointment"),
    path('add_document/<int:id_appointment>/', views.add_document, name="add_document")
]