import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir, os.pardir, os.pardir))
sys.path.append(project_root)
from constants import University


class UniversityViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('university_timetabling.timetable.views.timeslots_collection')
    def test_add_time_slot(self, mock_timeslots_collection):
        mock_timeslots_collection.has.return_value = False
        mock_timeslots_collection.insert.return_value = None

        data = {
            University.TIME_SLOTS: [{University.DAY: 'Monday', University.START_TIME: '09:00',
                                     University.END_TIME: '11:00'}, {University.DAY: 'Tuesday',
                                                                     University.START_TIME: '14:00',
                                                                     University.END_TIME: '16:00'}]
        }

        response = self.client.post(reverse('add_time_slot'), json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn('Time Slot(s) added successfully', response.json()['status'])

    @patch('university_timetabling.timetable.views.courses_collection')
    def test_add_course(self, mock_courses_collection):
        mock_courses_collection.has.return_value = False
        mock_courses_collection.insert.return_value = None

        data = {
            University.COURSE_NAME: 'Math',
            University.PREFERRED_TIME_SLOTS: [{University.DAY: 'Monday', University.START_TIME: '09:00',
                                               University.END_TIME: '11:00'}]
        }

        response = self.client.post(reverse('add_course'), json.dumps(data), content_type="application/json")

        mock_courses_collection.has.assert_called_with('Math')
        mock_courses_collection.insert.assert_called_once_with({
            University.KEY: 'Math',
            University.COURSE_NAME: 'Math',
            University.PREFERRED_TIME_SLOTS: [{'day': 'Monday', 'startTime': '09:00', 'endTime': '11:00'}]
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('Course added successfully', response.json()['status'])

    @patch('university_timetabling.timetable.views.courses_collection')
    @patch('university_timetabling.timetable.views.instructors_collection')
    def test_add_instructor(self, mock_instructors_collection, mock_courses_collection):
        def mock_get(course_name):
            if course_name == 'Math':
                return {
                    University.KEY: 'Math',
                    University.COURSE_NAME: 'Math',
                    University.PREFERRED_TIME_SLOTS: [{
                        University.DAY: 'Monday',
                        University.START_TIME: '09:00',
                        University.END_TIME: '11:00'
                    }]
                }
            return None

        mock_courses_collection.get.side_effect = mock_get

        mock_instructors_collection.has.return_value = False
        mock_instructors_collection.insert.return_value = None

        data = {
            University.NAME: 'James',
            University.PREFERRED_COURSES: [{University.COURSE_NAME: 'Math',
                                            University.PREFERRED_TIME_SLOTS: [{University.DAY: '',
                                                                               University.START_TIME: '',
                                                                               University.END_TIME: ''}]}],
            University.AVAILABILITY: [{University.DAY: 'Monday', University.START_TIME: '09:00',
                                       University.END_TIME: '11:00'}]
        }

        response = self.client.post(reverse('add_instructor'), json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn('Instructor added successfully', response.json()['status'])

    @patch('university_timetabling.timetable.views.instructors_collection')
    @patch('university_timetabling.timetable.views.courses_collection')
    @patch('university_timetabling.timetable.views.timeslots_collection')
    def test_generate_schedule(self, mock_timeslots_collection, mock_courses_collection, mock_instructors_collection):
        mock_instructors_collection.all.return_value = [
            {
                University.KEY: 'James',
                University.NAME: 'James',
                University.PREFERRED_COURSES: [{University.COURSE_NAME: 'Math',
                                                University.PREFERRED_TIME_SLOTS: [{University.DAY: '',
                                                                                   University.START_TIME: '',
                                                                                   University.END_TIME: ''}]}],
                University.AVAILABILITY: [{University.DAY: 'Monday', University.START_TIME: '09:00',
                                           University.END_TIME: '11:00'}]
            }
        ]

        mock_courses_collection.all.return_value = [
            {
                University.KEY: 'Math',
                University.COURSE_NAME: 'Math',
                University.PREFERRED_TIME_SLOTS: [{
                    University.DAY: 'Monday',
                    University.START_TIME: '09:00',
                    University.END_TIME: '11:00'
                }]
            }
        ]

        mock_timeslots_collection.all.return_value = [
            {
                University.KEY: 'Monday_09:00-11:00',
                University.DAY: 'Monday',
                University.START_TIME: '09:00',
                University.END_TIME: '11:00'
            },
            {
                University.KEY: 'Tuesday_14:00-16:00',
                University.DAY: 'Tuesday',
                University.START_TIME: '14:00',
                University.END_TIME: '16:00'
            }
        ]

        response = self.client.post(reverse('schedule'), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn('schedule', response.json())

    @patch('university_timetabling.timetable.views.courses_collection')
    @patch('university_timetabling.timetable.views.instructors_collection')
    @patch('university_timetabling.timetable.views.timeslots_collection')
    def test_show_university(self, mock_timeslots_collection, mock_instructors_collection, mock_courses_collection):
        mock_courses_collection.all.return_value = [{University.COURSE_NAME: "Math"}]
        mock_instructors_collection.all.return_value = [{University.NAME: "James"}]
        mock_timeslots_collection.all.return_value = [{University.DAY: "Monday", University.START_TIME: "08:00", University.END_TIME: "10:00"}]

        response = self.client.get(reverse('show_university'))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(University.COURSES, data)
        self.assertIn(University.INSTRUCTORS, data)
        self.assertIn(University.TIME_SLOTS, data)
        self.assertEqual(len(data[University.COURSES]), 1)
        self.assertEqual(len(data[University.INSTRUCTORS]), 1)
        self.assertEqual(len(data[University.TIME_SLOTS]), 1)


    @patch('university_timetabling.timetable.views.timeslots_collection')
    def test_add_time_slot_already_exists(self, mock_timeslots_collection):
        mock_timeslots_collection.has.return_value = True

        data = {
            University.TIME_SLOTS: [{University.DAY: 'Monday', University.START_TIME: '09:00',
                                     University.END_TIME: '11:00'}]
        }

        response = self.client.post(reverse('add_time_slot'), json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn('Time slot with this key already exists', response.json()['error'])

    @patch('university_timetabling.timetable.views.courses_collection')
    def test_add_course_with_invalid_data(self, mock_courses_collection):
        mock_courses_collection.has.return_value = False

        data = {
            University.COURSE_NAME: '',
            University.PREFERRED_TIME_SLOTS: [{University.DAY: 'Monday', University.START_TIME: '09:00',
                                               University.END_TIME: '11:00'}]
        }

        response = self.client.post(reverse('add_course'), json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing name', response.json()['error'])

    @patch('university_timetabling.timetable.views.timeslots_collection')
    @patch('university_timetabling.timetable.views.instructors_collection')
    def test_generate_schedule_with_empty_database(self, mock_instructors_collection, mock_timeslots_collection):
        mock_instructors_collection.all.return_value = []
        mock_timeslots_collection.all.return_value = []

        response = self.client.post(reverse('schedule'), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn('No data available in the database', response.json()['error'])

    @patch('university_timetabling.timetable.views.courses_collection')
    @patch('university_timetabling.timetable.views.instructors_collection')
    @patch('university_timetabling.timetable.views.timeslots_collection')
    def test_show_university_with_empty_database(self, mock_timeslots_collection, mock_instructors_collection, mock_courses_collection):
        mock_courses_collection.all.return_value = []
        mock_instructors_collection.all.return_value = []
        mock_timeslots_collection.all.return_value = []

        response = self.client.get(reverse('show_university'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('No data available in the database', response.content.decode())


if __name__ == '__main__':
    unittest.main()