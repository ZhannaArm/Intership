# backend/university_timetabling/timetable/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('add-course/', views.add_course, name='add_course'),
    path('add-instructor/', views.add_instructor, name='add_instructor'),
    path('add-time-slot/', views.add_time_slot, name='add_time_slot'),
    path('schedule/', views.generate_schedule, name='schedule'),
    path('show-university/', views.show_university, name='show_university'),
]

