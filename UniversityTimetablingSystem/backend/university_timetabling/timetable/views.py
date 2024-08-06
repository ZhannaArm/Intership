# backend/university_timetabling/timetable/views.py

from django.shortcuts import render
import sys
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
import subprocess

# sys.path.append('/Users/apple/intership/UniversityTimetablingSystem/build/')
# try:
#     import university_bindings as ub
# except ImportError as e:
#     raise ImportError(f"Failed to import university_bindings: {e}")
#
# university = ub.University()
# university.loadState("result.json")

@csrf_exempt
def add_instructor(request):
    if request.method == 'POST':
        try:
            # data = json.loads(request.body)
            # name = data.get('name')
            # preferred_courses_data = data.get('preferred_courses', [])
            # availability_data = data.get('availability', [])
            #
            # if not name:
            #     return JsonResponse({'status': 'Error', 'message': 'Missing name'}, status=400)
            #
            # availability = [ub.TimeSlot(slot['day'], slot['startTime'], slot['endTime']) for slot in availability_data]
            #
            # preferred_courses = []
            # for course_data in preferred_courses_data:
            #     print(f"Processing course data: {course_data}")
            #
            #     course_name = course_data.get('courseName')
            #
            #     if not university.courseExists(course_name):
            #         return JsonResponse({'status': 'Error', 'message': f'Course {course_name} does not exist'}, status=400)
            #
            #     try:
            #         course = university.getCourse(course_name)
            #     except Exception as e:
            #         return JsonResponse({'status': 'Error', 'message': str(e)}, status=400)
            #
            #     preferred_courses.append(course)
            #
            # instructor = ub.Instructor(name, availability, preferred_courses)
            # university.addInstructor(instructor)
            #
            # university.saveState('result.json')

            data = json.loads(request.body)
            name = data.get('name')
            preferred_courses_data = data.get('preferred_courses', [])
            availability_data = data.get('availability', [])

            if not name:
                return JsonResponse({'status': 'Error', 'message': 'Missing name'}, status=400)

            args = [
                '/Users/apple/intership/UniversityTimetablingSystem/build/UniversityTimetablingSystem',
                '--addInstructor',
                json.dumps({
                    'name': name,
                    'preferred_courses': preferred_courses_data,
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
            # data = json.loads(request.body)
            #
            # name = data.get('name')
            # preferred_time_slots_data = data.get('preferred_time_slots', [])
            #
            # if not name:
            #     return JsonResponse({'status': 'Error', 'message': 'Missing name'}, status=400)
            #
            # preferred_time_slots = [ub.TimeSlot(slot['day'], slot['startTime'], slot['endTime']) for slot in preferred_time_slots_data]
            #
            # course = ub.Course(name, preferred_time_slots)
            # university.addCourse(course)
            # university.saveState('result.json')

            data = json.loads(request.body)
            name = data.get('name')
            preferred_time_slots_data = data.get('preferred_time_slots', [])

            if not name:
                return JsonResponse({'status': 'Error', 'message': 'Missing name'}, status=400)

            args = [
                '/Users/apple/intership/UniversityTimetablingSystem/build/UniversityTimetablingSystem',
                '--addCourse',
                json.dumps({
                    'name': name,
                    'preferred_time_slots': preferred_time_slots_data
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
            # data = json.loads(request.body)
            # if 'time_slots' not in data:
            #     return JsonResponse({'status': 'Error', 'message': 'No time_slots in request body'}, status=400)
            #
            # for ts in data['time_slots']:
            #     day = ts.get('day')
            #     start_time = ts.get('startTime')
            #     end_time = ts.get('endTime')
            #
            #     if not day or not start_time or not end_time:
            #         return JsonResponse({'status': 'Error', 'message': 'Missing fields in time slot'}, status=400)
            #
            #     time_slot = ub.TimeSlot(day, start_time, end_time)
            #     university.addTimeSlot(time_slot)
            # university.saveState('result.json')

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
            # university = ub.University()
            # university.loadState('result.json')
            #
            # university_map = university.schedule()
            # schedule_data = university.scheduleToJsonFormat()
            #
            # if not schedule_data:
            #     #print("Debug: schedule_data is empty")
            #     return JsonResponse({'error': 'No schedule data available'}, status=500)
            #
            # university.saveState('result.json')
            #
            # schedule = [{'course': course, 'timeSlot': timeSlot, 'instructor': instructor}
            #             for course, timeSlot, instructor in schedule_data]

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
        # university = ub.University()
        # university.loadState('result.json')
        #
        # courses = [{'name': course.getCourseName()} for course in university.getCourses()]
        # instructors = [{'name': instructor.getName()} for instructor in university.getInstructors()]
        # time_slots = [{'day': slot.getDay(), 'startTime': slot.getStartTime(), 'endTime': slot.getEndTime()} for slot in university.getTimeSlots()]
        #
        # return JsonResponse({
        #     'courses': courses,
        #     'instructors': instructors,
        #     'timeSlots': time_slots
        # })

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