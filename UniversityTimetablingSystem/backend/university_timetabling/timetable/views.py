# backend/university_timetabling/timetable/views.py

from django.shortcuts import render
import os
import sys
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from arango import ArangoClient
import json
import traceback


client = ArangoClient(hosts="http://localhost:8529")
sys_db = client.db('_system', username='root', password='openSesame')

if not sys_db.has_database('university_db'):
    sys_db.create_database('university_db')

db = client.db('university_db', username='root', password='openSesame')

if not db.has_collection('instructors'):
    instructors_collection = db.create_collection('instructors')
else:
    instructors_collection = db.collection('instructors')

if not db.has_collection('courses'):
    courses_collection = db.create_collection('courses')
else:
    courses_collection = db.collection('courses')

if not db.has_collection('timeslots'):
    timeslots_collection = db.create_collection('timeslots')
else:
    timeslots_collection = db.collection('timeslots')

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir, os.pardir, "build"))
sys.path.append(project_root)

try:
    import university_bindings as ub
except ImportError as e:
    raise ImportError(f"Failed to import university_bindings: {e}")

university = ub.University()


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

            availability = []
            for slot in availability_data:
                time_slot = {
                    'day': slot['day'],
                    'startTime': slot['startTime'],
                    'endTime': slot['endTime']
                }
                if not all(time_slot.values()):
                    return HttpResponseBadRequest('Missing fields in availability slot')
                availability.append(time_slot)

            preferred_courses = []
            for course_data in preferred_courses_data:
                if 'courseName' not in course_data:
                    return HttpResponseBadRequest('Missing courseName in preferredCourses')

                course_name = course_data['courseName']
                if not course_name:
                    return HttpResponseBadRequest('Course name cannot be empty')

                print(f"Processing course: {course_name}")

                try:
                    course_doc = db.collection('courses').get(course_name)
                    print(course_doc)
                    if not course_doc:
                        return HttpResponseBadRequest(f"Course {course_name} does not exist in the database.")
                except Exception as e:
                    return HttpResponseBadRequest(f"Error retrieving course {course_name}: {str(e)}")

                try:
                    time_slots = course_doc.get('preferredTimeSlots', [])
                    preferred_time_slots = [{
                        'day': slot['day'],
                        'startTime': slot['startTime'],
                        'endTime': slot['endTime']
                    } for slot in time_slots]

                    course = {
                        'courseName': course_doc['courseName'],
                        'preferredTimeSlots': preferred_time_slots
                    }
                    preferred_courses.append(course)
                except Exception as e:
                    return HttpResponseBadRequest(f"Error creating Course object for {course_name}: {str(e)}")

            instructor = {
                '_key': name,
                'name': name,
                'preferredCourses': preferred_courses,
                'availability': availability
            }

            if instructors_collection.has(instructor['_key']):
                return HttpResponseBadRequest('Instructor with this name already exists')
            instructors_collection.insert(instructor)

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

            course = {
                '_key': name,
                'courseName': name,
                'preferredTimeSlots': preferred_time_slots_data
            }

            if courses_collection.has(course['_key']):
                return HttpResponseBadRequest('Course with this name already exists')
            courses_collection.insert(course)

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

                time_slot_key = f"{day}_{start_time}-{end_time}"

                time_slot = {
                    '_key': time_slot_key,
                    'day': day,
                    'startTime': start_time,
                    'endTime': end_time
                }

                if timeslots_collection.has(time_slot['_key']):
                    return HttpResponseBadRequest('Time slot with this key already exists')
                timeslots_collection.insert(time_slot)

            return JsonResponse({'status': 'Time Slot(s) added successfully'})
        except Exception as e:
            print(f"Error occurred: {e}")
            return HttpResponseServerError(str(e))
    return HttpResponseBadRequest('Invalid request method')


@csrf_exempt
def generate_schedule(request):
    if request.method == 'POST':
        try:
            collections = ['courses', 'instructors', 'timeslots']
            for collection in collections:
                if not db.has_collection(collection):
                    db.create_collection(collection)

            courses = list(db.collection('courses').all())
            instructors = list(db.collection('instructors').all())
            time_slots = list(db.collection('timeslots').all())

            py_courses = []
            for c in courses:
                course_name = c.get('courseName')
                preferred_time_slots = c.get('preferredTimeSlots', [])

                if not course_name:
                    print(f"Skipping course due to missing 'courseName': {c}")
                    continue

                preferredTimeSlots = [ub.TimeSlot(slot['day'], slot['startTime'], slot['endTime']) for slot in preferred_time_slots]
                py_courses.append(ub.Course(course_name, preferredTimeSlots))

            py_instructors = []
            for i in instructors:
                name = i.get('name')
                availability_data = i.get('availability', [])
                preferred_courses_data = i.get('preferredCourses', [])

                if not name:
                    print(f"Skipping instructor due to missing 'name': {i}")
                    continue

                availability = [ub.TimeSlot(slot['day'], slot['startTime'], slot['endTime']) for slot in availability_data]
                print(availability)

                preferred_courses = []
                for course_data in preferred_courses_data:
                    course_name = course_data.get('courseName')
                    if not course_name:
                        print(f"Skipping preferred course due to missing 'courseName': {course_data}")
                        continue

                    course = next((c for c in py_courses if c.getCourseName() == course_name), None)
                    if not course:
                        print(f"Course {course_name} not found in py_courses")
                        continue

                    preferred_courses.append(course)

                py_instructors.append(ub.Instructor(name, availability, preferred_courses))

            py_time_slots = []
            for t in time_slots:
                day = t.get('day')
                start_time = t.get('startTime')
                end_time = t.get('endTime')

                py_time_slots.append(ub.TimeSlot(day, start_time, end_time))

            university = ub.University()
            for course in py_courses:
                university.addCourse(course)
            for instructor in py_instructors:
                university.addInstructor(instructor)
            for time_slot in py_time_slots:
                university.addTimeSlot(time_slot)

            schedule = university.schedule()
            schedule_data = university.scheduleToJsonFormat()
            return JsonResponse({'schedule': schedule_data})
        except Exception as e:
            traceback.print_exc()
            return HttpResponseServerError(str(e))
    else:
        return HttpResponseBadRequest('Invalid request method')


@csrf_exempt
def show_university(request):
    try:
        courses = list(db.collection('courses').all())
        instructors = list(db.collection('instructors').all())
        time_slots = list(db.collection('timeslots').all())

        return JsonResponse({
            'courses': courses,
            'instructors': instructors,
            'timeSlots': time_slots
        })

    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return HttpResponseServerError(str(e))