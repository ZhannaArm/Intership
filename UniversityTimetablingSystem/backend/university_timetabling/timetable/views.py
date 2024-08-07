# backend/university_timetabling/timetable/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
import subprocess

@csrf_exempt
def add_instructor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            preferred_courses_data = data.get('preferredCourses', [])
            availability_data = data.get('availability', [])

            if not name:
                return JsonResponse({'status': 'Error', 'message': 'Missing name'}, status=400)

            args = [
                '/Users/apple/intership/UniversityTimetablingSystem/build/UniversityTimetablingSystem',
                '--addInstructor',
                json.dumps({
                    'name': name,
                    'preferredCourses': preferred_courses_data,
                    'availability': availability_data
                })
            ]

            result = subprocess.run(args, capture_output=True, text=True, check=True)
            print('Output:', result.stdout)

            return JsonResponse({'status': 'Instructor added successfully'})
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=400)
        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'Invalid request method'}, status=405)


@csrf_exempt
def add_course(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('courseName')
            preferred_time_slots_data = data.get('preferredTimeSlots', [])

            if not name:
                return JsonResponse({'status': 'Error', 'message': 'Missing name'}, status=400)

            args = [
                '/Users/apple/intership/UniversityTimetablingSystem/build/UniversityTimetablingSystem',
                '--addCourse',
                json.dumps({
                    'courseName': name,
                    'preferredTimeSlots': preferred_time_slots_data
                })
            ]

            result = subprocess.run(args, capture_output=True, text=True, check=True)
            print('Output:', result.stdout)

            return JsonResponse({'status': 'Course added successfully'})
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=400)
        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'Invalid request method'}, status=405)

@csrf_exempt
def add_time_slot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if 'time_slots' not in data:
                return JsonResponse({'status': 'Error', 'message': 'No time_slots in request body'}, status=400)

            args = [
                '/Users/apple/intership/UniversityTimetablingSystem/build/UniversityTimetablingSystem',
                '--addTimeSlot',
                json.dumps(data['time_slots'])
            ]


            result = subprocess.run(args, capture_output=True, text=True, check=True)
            print('Output:', result.stdout)

            return JsonResponse({'status': 'Time Slot(s) added successfully'})
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'Invalid request method'}, status=405)

@csrf_exempt
def generate_schedule(request):
    if request.method == 'POST':
        try:
            args = [
                '/Users/apple/intership/UniversityTimetablingSystem/build/UniversityTimetablingSystem',
                '--schedule'
            ]

            result = subprocess.run(args, capture_output=True, text=True, check=True)
            print('Output:', result.stdout)

            schedule = json.loads(result.stdout)
            if not schedule:
                return JsonResponse({'error': 'No schedule data available'}, status=500)

            return JsonResponse({'schedule': schedule})
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def show_university(request):
    try:
        args = [
            '/Users/apple/intership/UniversityTimetablingSystem/build/UniversityTimetablingSystem',
            '--showUniversity'
        ]

        result = subprocess.run(args, capture_output=True, text=True, check=True)
        print('Output:', result.stdout)

        university_data = json.loads(result.stdout)
        return JsonResponse(university_data)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)
    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)