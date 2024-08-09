# backend/university_timetabling/timetable/models.py

from django.db import models

class TimeSlot(models.Model):
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day} {self.start_time}-{self.end_time}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    preferred_time_slots = models.ManyToManyField(TimeSlot, blank=True)

    def __str__(self):
        return self.name

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    preferred_courses = models.ManyToManyField(Course, blank=True)
    availability = models.ManyToManyField(TimeSlot, blank=True)

    def __str__(self):
        return self.name

class University(models.Model):
    courses = models.ManyToManyField(Course, related_name="university")
    instructors = models.ManyToManyField(Instructor, related_name="university")
    time_slots = models.ManyToManyField(TimeSlot, related_name="university")

    def displayInfo(self):
        print("University Information:")
        print("Courses:")
        for course in self.courses.all():
            print(course)
        print("\nInstructors:")
        for instructor in self.instructors.all():
            print(instructor)
        print("\nTimeSlots:")
        for time_slot in self.time_slots.all():
            print(time_slot)