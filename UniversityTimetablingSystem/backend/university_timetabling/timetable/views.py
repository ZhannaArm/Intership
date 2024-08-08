# backend/university_timetabling/timetable/views.py

from django.shortcuts import render
import os
import sys
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import json
import traceback

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../../build'))
sys.path.append(project_root)

try:
    import university_bindings as ub
except ImportError as e:
    raise ImportError(f"Failed to import university_bindings: {e}")

university = ub.University()
university.loadState("result.json")

@csrf_exempt
def add_instructor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            preferred_courses_data = data.get('preferredCourses', [])
            availability_data = data.get('availability', [])

            if not name:
                return HttpResponseBadRequest('Missing name')

            availability = [ub.TimeSlot(slot['day'], slot['startTime'], slot['endTime']) for slot in availability_data]

            preferred_courses = []
            for course_data in preferred_courses_data:
                print(f"Processing course data: {course_data}")

                course_name = course_data.get('courseName')

                if not university.courseExists(course_name):
                    return HttpResponseBadRequest(f'Course {course_name} does not exist')

                try:
                    course = university.getCourse(course_name)
                except Exception as e:
                    return HttpResponseBadRequest(str(e))

                preferred_courses.append(course)

            instructor = ub.Instructor(name, availability, preferred_courses)
            university.addInstructor(instructor)

            university.saveState('result.json')

            return JsonResponse({'status': 'Instructor added successfully'})
        except Exception as e:
            print(f"Error occurred: {e}")
            return HttpResponseServerError(str(e))
    return HttpResponseBadRequest('Invalid request method')


@csrf_exempt
def add_course(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('courseName')
            preferred_time_slots_data = data.get('preferredTimeSlots', [])

            if not name:
                return HttpResponseBadRequest('Missing name')

            preferred_time_slots = [ub.TimeSlot(slot['day'], slot['startTime'], slot['endTime']) for slot in preferred_time_slots_data]

            course = ub.Course(name, preferred_time_slots)
            university.addCourse(course)
            university.saveState('result.json')

            return JsonResponse({'status': 'Course added successfully'})
        except Exception as e:
            print(f"Error occurred: {e}")
            return HttpResponseServerError(str(e))
    return HttpResponseBadRequest('Invalid request method')

@csrf_exempt
def add_time_slot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if 'time_slots' not in data:
                return HttpResponseBadRequest('No time_slots in request body')

            for ts in data['time_slots']:
                day = ts.get('day')
                start_time = ts.get('startTime')
                end_time = ts.get('endTime')

                if not day or not start_time or not end_time:
                    return HttpResponseBadRequest('Missing fields in time slot')

                time_slot = ub.TimeSlot(day, start_time, end_time)
                university.addTimeSlot(time_slot)

            university.saveState('result.json')

            return JsonResponse({'status': 'Time Slot(s) added successfully'})
        except Exception as e:
            print(f"Error occurred: {e}")
            return HttpResponseServerError(str(e))
    return HttpResponseBadRequest('Invalid request method')

@csrf_exempt
def generate_schedule(request):
    if request.method == 'POST':
        try:
            university = ub.University()
            university.loadState('result.json')

            university_map = university.schedule()
            schedule_data = university.scheduleToJsonFormat()

            if not schedule_data:
                return HttpResponseServerError('No schedule data available')

            university.saveState('result.json')

            schedule = [{'course': course, 'timeSlot': timeSlot, 'instructor': instructor}
                        for course, timeSlot, instructor in schedule_data]

            return JsonResponse({'schedule': schedule})
        except Exception as e:
            traceback.print_exc()
            return HttpResponseServerError(str(e))
    else:
        return HttpResponseBadRequest('Invalid request method')

@csrf_exempt
def show_university(request):
    try:
        university = ub.University()
        university.loadState('result.json')

        courses = [{'courseName': course.getCourseName()} for course in university.getCourses()]
        instructors = [{'name': instructor.getName()} for instructor in university.getInstructors()]
        time_slots = [{'day': slot.getDay(), 'startTime': slot.getStartTime(), 'endTime': slot.getEndTime()} for slot in university.getTimeSlots()]

        return JsonResponse({
            'courses': courses,
            'instructors': instructors,
            'timeSlots': time_slots
        })

    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return HttpResponseServerError(str(e))