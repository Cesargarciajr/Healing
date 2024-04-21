from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('booking/<int:id_doctors_data>/', views.booking, name="booking"),
    path('appointment/<int:id_schedule>', views.appointment, name="appointment"),
    path('my_bookings/', views.my_bookings, name="my_bookings"),
    path('access_appointment/<int:id_appointment>/', views.access_appointment, name="access_appointment"),
]
