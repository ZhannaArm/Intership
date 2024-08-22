import os
import sys
import json
import traceback
from arango import ArangoClient
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir, os.pardir))
sys.path.append(project_root)
from constants import University

client = ArangoClient(hosts="http://localhost:8529")
sys_db = client.db('_system', username='root', password='openSesame')
db = client.db(University.UNIVERSITY, username='root', password='openSesame')

instructors_collection = db.collection(University.INSTRUCTORS)
courses_collection = db.collection(University.COURSES)
timeslots_collection = db.collection(University.TIME_SLOTS)

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir, os.pardir, 'build'))
sys.path.append(project_root)

try:
    import university_bindings as ub
except ImportError as e:
    raise ImportError(f"Failed to import university_bindings: {e}")

university = ub.University()


@csrf_exempt
def add_instructor(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')
    try:
        data = json.loads(request.body)
        name = data.get(University.NAME)
        preferred_courses_data = data.get(University.PREFERRED_COURSES, [])
        availability_data = data.get(University.AVAILABILITY, [])

        if not name:
            return HttpResponseBadRequest('Missing name')

        availability = process_availability(availability_data)
        if availability is None:
            return HttpResponseBadRequest('Invalid availability data')

        preferred_courses = process_preferred_courses(preferred_courses_data)
        if preferred_courses is None:
            return HttpResponseBadRequest('Invalid preferred courses data')

        if instructor_exists(name):
            return HttpResponseBadRequest('Instructor with this name already exists')

        create_and_add_instructor(name, preferred_courses, availability)

        return JsonResponse({'status': 'Instructor added successfully'})
    except Exception as e:
        print(f"Error occurred: {e}")
        return HttpResponseServerError(str(e))


def process_availability(availability_data):
    availability = []
    for slot in availability_data:
        time_slot = {
            University.DAY: slot[University.DAY],
            University.START_TIME: slot[University.START_TIME],
            University.END_TIME: slot[University.END_TIME]
        }
        if not all(time_slot.values()):
            return None
        availability.append(time_slot)
    return availability


def process_preferred_courses(preferred_courses_data):
    preferred_courses = []
    for course_data in preferred_courses_data:
        course_name = course_data.get(University.COURSE_NAME)
        
        if not course_name:
            print("Error: Missing or empty course name in preferredCourses")
            return None

        print(f"Processing course: {course_name}")

        course_doc = db.collection(University.COURSES).get(course_name)
        if not course_doc:
            print(f"Error: Course {course_name} does not exist in the database.")
            return None

        time_slots = course_doc.get(University.PREFERRED_TIME_SLOTS, [])

        preferred_time_slots = [{
            University.DAY: slot[University.DAY],
            University.START_TIME: slot[University.START_TIME],
            University.END_TIME: slot[University.END_TIME]
        } for slot in time_slots]

        course = {
            University.COURSE_NAME: course_doc[University.COURSE_NAME],
            University.PREFERRED_TIME_SLOTS: preferred_time_slots
        }
        preferred_courses.append(course)

    return preferred_courses


def instructor_exists(name):
    return instructors_collection.has(name)


def create_and_add_instructor(name, preferred_courses, availability):
    instructor = {
        University.KEY: name,
        University.NAME: name,
        University.PREFERRED_COURSES: preferred_courses,
        University.AVAILABILITY: availability
    }
    instructors_collection.insert(instructor)


@csrf_exempt
def add_course(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')
    try:
        data = json.loads(request.body)

        name = data.get(University.COURSE_NAME)
        preferred_time_slots_data = data.get(University.PREFERRED_TIME_SLOTS, [])

        if not name:
            return HttpResponseBadRequest('Missing name')

        if course_exists(name):
            return HttpResponseBadRequest('Course with this name already exists')

        create_and_add_course(name, preferred_time_slots_data)

        return JsonResponse({'status': 'Course added successfully'})
    except Exception as e:
        print(f"Error occurred: {e}")
        return HttpResponseServerError(str(e))


def course_exists(name):
    return courses_collection.has(name)


def create_and_add_course(name, preferred_time_slots_data):
    course = {
        University.KEY: name,
        University.COURSE_NAME: name,
        University.PREFERRED_TIME_SLOTS: preferred_time_slots_data
    }
    courses_collection.insert(course)


@csrf_exempt
def add_time_slot(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')
    try:
        data = json.loads(request.body)
        if University.TIME_SLOTS not in data:
            return HttpResponseBadRequest('No time_slots in request body')

        for timeSlot in data[University.TIME_SLOTS]:
            day = timeSlot.get(University.DAY)
            start_time = timeSlot.get(University.START_TIME)
            end_time = timeSlot.get(University.END_TIME)

            if not day or not start_time or not end_time:
                return HttpResponseBadRequest('Missing fields in time slot')

            time_slot_key = f"{day}_{start_time}-{end_time}"

            if time_slot_exists(time_slot_key):
                return HttpResponseBadRequest('Time slot with this key already exists')

            create_and_add_time_slot(time_slot_key, day, start_time, end_time)

        return JsonResponse({'status': 'Time Slot(s) added successfully'})
    except Exception as e:
        print(f"Error occurred: {e}")
        return HttpResponseServerError(str(e))


def time_slot_exists(time_slot_key):
    return timeslots_collection.has(time_slot_key)


def create_and_add_time_slot(time_slot_key, day, start_time, end_time):
    time_slot = {
        University.KEY: time_slot_key,
        University.DAY: day,
        University.START_TIME: start_time,
        University.END_TIME: end_time
    }
    timeslots_collection.insert(time_slot)


@csrf_exempt
def generate_schedule(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')
    try:
        py_courses = load_courses()
        py_instructors = load_instructors(py_courses)
        py_time_slots = load_time_slots()

        university = build_university(py_courses, py_instructors, py_time_slots)

        schedule_data = generate_university_schedule(university)
        return JsonResponse({University.SCHEDULE: schedule_data})
    except Exception as e:
        traceback.print_exc()
        return HttpResponseServerError(str(e))


def load_courses():
    courses = list(db.collection(University.COURSES).all())
    py_courses = []
    for course in courses:
        course_name = course.get(University.COURSE_NAME)
        preferred_time_slots = course.get(University.PREFERRED_TIME_SLOTS, [])

        if not course_name:
            print(f"Skipping course due to missing 'courseName': {course}")
            continue

        preferredTimeSlots = [
            ub.TimeSlot(slot[University.DAY], slot[University.START_TIME], slot[University.END_TIME])
            for slot in preferred_time_slots
        ]
        py_courses.append(ub.Course(course_name, preferredTimeSlots))

    return py_courses


def load_instructors(py_courses):
    instructors = list(db.collection(University.INSTRUCTORS).all())
    py_instructors = []
    for instructor in instructors:
        name = instructor.get(University.NAME)
        availability_data = instructor.get(University.AVAILABILITY, [])
        preferred_courses_data = instructor.get(University.PREFERRED_COURSES, [])

        if not name:
            print(f"Skipping instructor due to missing 'name': {instructor}")
            continue

        availability = [
            ub.TimeSlot(slot[University.DAY], slot[University.START_TIME], slot[University.END_TIME])
            for slot in availability_data
        ]

        preferred_courses = []
        for course_data in preferred_courses_data:
            course_name = course_data.get(University.COURSE_NAME)
            if not course_name:
                print(f"Skipping preferred course due to missing 'courseName': {course_data}")
                continue

            course = next((c for c in py_courses if c.getCourseName() == course_name), None)
            if not course:
                print(f"Course {course_name} not found in py_courses")
                continue

            preferred_courses.append(course)

        py_instructors.append(ub.Instructor(name, availability, preferred_courses))

    return py_instructors


def load_time_slots():
    time_slots = list(db.collection(University.TIME_SLOTS).all())
    py_time_slots = []
    for timeSlot in time_slots:
        day = timeSlot.get(University.DAY)
        start_time = timeSlot.get(University.START_TIME)
        end_time = timeSlot.get(University.END_TIME)

        py_time_slots.append(ub.TimeSlot(day, start_time, end_time))

    return py_time_slots


def build_university(py_courses, py_instructors, py_time_slots):
    university = ub.University()
    for course in py_courses:
        university.addCourse(course)
    for instructor in py_instructors:
        university.addInstructor(instructor)
    for time_slot in py_time_slots:
        university.addTimeSlot(time_slot)

    return university


def generate_university_schedule(university):
    schedule = university.schedule()
    return university.scheduleToJsonFormat()


@csrf_exempt
def show_university(request):
    try:
        courses = list(db.collection(University.COURSES).all())
        instructors = list(db.collection(University.INSTRUCTORS).all())
        time_slots = list(db.collection(University.TIME_SLOTS).all())

        return JsonResponse({
            University.COURSES: courses,
            University.INSTRUCTORS: instructors,
            University.TIME_SLOTS: time_slots
        })

    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return HttpResponseServerError(str(e))