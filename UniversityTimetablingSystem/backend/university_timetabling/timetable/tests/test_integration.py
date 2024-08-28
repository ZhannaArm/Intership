import os
import sys
import json
from django.test import TestCase
from django.urls import reverse
from arango import ArangoClient

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir, os.pardir, os.pardir))
sys.path.append(project_root)
from constants import University


class UniversityIntegrationTest(TestCase):
    def setUp(self):
        self.client_db = ArangoClient(hosts="http://localhost:8529")
        self.db = self.client_db.db(University.UNIVERSITY, username='root', password='openSesame')

        self.instructors_collection = self.db.collection(University.INSTRUCTORS)
        self.courses_collection = self.db.collection(University.COURSES)
        self.timeslots_collection = self.db.collection(University.TIME_SLOTS)

        self.instructor_data = {
            University.NAME: 'James',
            University.PREFERRED_COURSES: [{University.COURSE_NAME: 'Math',
                                            University.PREFERRED_TIME_SLOTS: [{University.DAY: '',
                                                                               University.START_TIME: '',
                                                                               University.END_TIME: ''}]}],
            University.AVAILABILITY: [{University.DAY: 'Monday', University.START_TIME: '09:00',
                                       University.END_TIME: '11:00'}]
        }

        self.course_data = {
            University.COURSE_NAME: 'Math',
            University.PREFERRED_TIME_SLOTS: [{University.DAY: 'Monday', University.START_TIME: '09:00',
                                               University.END_TIME: '11:00'}]
        }

        self.time_slot_data = {
            University.TIME_SLOTS: [{University.DAY: 'Monday', University.START_TIME: '09:00',
                                     University.END_TIME: '11:00'}]
        }

    def test_add_time_slot(self):
        response = self.client.post(reverse('add_time_slot'), json.dumps(self.time_slot_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        time_slot = self.db.collection(University.TIME_SLOTS).get("Monday_09:00-11:00")
        self.assertIsNotNone(time_slot)

    def test_add_course(self):
        response = self.client.post(reverse('add_course'), json.dumps(self.course_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        course = self.db.collection(University.COURSES).get('Math')
        self.assertIsNotNone(course)

    def test_add_instructor(self):
        response = self.client.post(reverse('add_instructor'), json.dumps(self.instructor_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        instructor = self.db.collection(University.INSTRUCTORS).get('James')
        self.assertIsNotNone(instructor)

    def test_generate_schedule(self):
        self.client.post(reverse('add_time_slot'), json.dumps(self.time_slot_data), content_type='application/json')
        self.client.post(reverse('add_course'), json.dumps(self.course_data), content_type='application/json')
        self.client.post(reverse('add_instructor'), json.dumps(self.instructor_data), content_type='application/json')

        response = self.client.post(reverse('schedule'))
        self.assertEqual(response.status_code, 200)
        schedule = response.json()
        self.assertIn(University.SCHEDULE, schedule)

        schedule_list = schedule[University.SCHEDULE]
        self.assertGreater(len(schedule_list), 0, 'Schedule list is empty')

        course_entry = next((entry for entry in schedule_list if entry[0] == 'Math'), None)
        self.assertIsNotNone(course_entry, 'Course Math not found in schedule')
        self.assertEqual(course_entry[1], 'Monday 09:00-11:00', 'Incorrect time slot for Math course')
        self.assertEqual(course_entry[2], 'James', 'Incorrect instructor for Math course')

    def test_add_instructor_with_missing_name(self):
        invalid_instructor_data = {
            University.PREFERRED_COURSES: [{University.COURSE_NAME: 'Math',
                                            University.PREFERRED_TIME_SLOTS: [{University.DAY: '',
                                                                               University.START_TIME: '',
                                                                               University.END_TIME: ''}]}],
            University.AVAILABILITY: [{University.DAY: 'Monday', University.START_TIME: '09:00',
                                       University.END_TIME: '11:00'}]
        }

        response = self.client.post(reverse('add_instructor'), json.dumps(invalid_instructor_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing name', response.content.decode())

    def test_add_course_with_invalid_data(self):
        invalid_course_data = {
            University.PREFERRED_TIME_SLOTS: [{University.DAY: 'Monday', University.START_TIME: '09:00',
                                               University.END_TIME: '11:00'}]
        }

        response = self.client.post(reverse('add_course'), json.dumps(invalid_course_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing name', response.content.decode())

    def test_generate_schedule_with_empty_database(self):
        self.instructors_collection.truncate()
        self.courses_collection.truncate()
        self.timeslots_collection.truncate()

        response = self.client.post(reverse('schedule'))

        # self.assertEqual(response.status_code, 500)
        self.assertIn('No data available in the database', response.content.decode())