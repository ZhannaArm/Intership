# backend/university_timetabling/timetable/views.py

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import os
import json
import traceback
import subprocess

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir, os.pardir, 'bin'))

@csrf_exempt
def add_instructor(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')
    try:
        data = json.loads(request.body)
        name = data.get('name')
        preferred_courses_data = data.get('preferredCourses', [])
        availability_data = data.get('availability', [])

        if not name:
            return HttpResponseBadRequest('Missing name')

        args = [
            os.path.join(project_root, 'UniversityTimetablingSystem'),
            '--addInstructor',
            name,
            '--preferredCourses',
        ]

        for course in preferred_courses_data:
            args.extend([course['courseName']])

        args.extend(['--availability'])
        for slot in availability_data:
            args.extend([slot['day'], slot['startTime'], slot['endTime']])

        result = subprocess.run(args, capture_output=True, text=True, check=True)
        print('Output:', result.stdout)

        return JsonResponse({'status': 'Instructor added successfully'})
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return HttpResponseBadRequest(f"Error occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
        return HttpResponseBadRequest(f"Error occurred: {e}")

@csrf_exempt
def add_course(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')
    try:
        data = json.loads(request.body)
        name = data.get('courseName')
        preferred_time_slots_data = data.get('preferredTimeSlots', [])

        if not name:
            return HttpResponseBadRequest('Missing name')

        args = [
            os.path.join(project_root, 'UniversityTimetablingSystem'),
            '--addCourse',
            name,
            '--preferredTimeSlots',
        ]

        for slot in preferred_time_slots_data:
            args.extend([slot['day'], slot['startTime'], slot['endTime']])

        result = subprocess.run(args, capture_output=True, text=True, check=True)
        print('Output:', result.stdout)

        return JsonResponse({'status': 'Course added successfully'})
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return HttpResponseBadRequest(f"Error occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
        return HttpResponseBadRequest(f"Error occurred: {e}")

@csrf_exempt
def add_time_slot(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')
    try:
        data = json.loads(request.body)
        if 'time_slots' not in data:
            return HttpResponseBadRequest('No time_slots in request body')

        args = [
            os.path.join(project_root, 'UniversityTimetablingSystem'),
            '--addTimeSlot',
        ]

        for slot in data['time_slots']:
            args.extend([slot['day'], slot['startTime'], slot['endTime']])

        result = subprocess.run(args, capture_output=True, text=True, check=True)
        print('Output:', result.stdout)

        return JsonResponse({'status': 'Time Slot(s) added successfully'})
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return HttpResponseBadRequest(f"Error occurred: {e}")
    except Exception as e:
        return HttpResponseBadRequest(f"Error occurred: {e}")

@csrf_exempt
def generate_schedule(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')
    try:
        args = [
            os.path.join(project_root, 'UniversityTimetablingSystem'),
            '--schedule'
        ]

        result = subprocess.run(args, capture_output=True, text=True, check=True)
        print('Output:', result.stdout)

        schedule = json.loads(result.stdout)
        if not schedule:
            return HttpResponseServerError('No schedule data available')

        return JsonResponse({'schedule': schedule})
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return HttpResponseServerError(f"Error occurred: {e}")
    except Exception as e:
        traceback.print_exc()
        return HttpResponseServerError(f"Error occurred: {e}")

@csrf_exempt
def show_university(request):
    try:
        args = [
            os.path.join(project_root, 'UniversityTimetablingSystem'),
            '--showUniversity'
        ]

        result = subprocess.run(args, capture_output=True, text=True, check=True)
        print('Output:', result.stdout)

        university_data = json.loads(result.stdout)
        return JsonResponse(university_data)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return HttpResponseServerError(f"Error occurred: {e}")
    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return HttpResponseServerError(f"Exception occurred: {e}")
