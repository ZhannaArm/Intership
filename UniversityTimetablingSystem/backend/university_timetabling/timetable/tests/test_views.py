import json
import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse


class UniversityViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('university_timetabling.timetable.views.instructors_collection')
    def test_add_instructor(self, mock_instructors_collection):
        mock_instructors_collection.has.return_value = False
        mock_instructors_collection.insert.return_value = None

        data = {
            "name": "James",
            "preferredCourses": [{"courseName": "Math"}],
            "availability": [{"day": "Monday", "startTime": "08:00", "endTime": "10:00"}]
        }

        response = self.client.post(reverse('add_instructor'), json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn('Instructor added successfully', response.json()['status'])

    @patch('university_timetabling.timetable.views.courses_collection')
    def test_add_course(self, mock_courses_collection):
        mock_courses_collection.has.return_value = False
        mock_courses_collection.insert.return_value = None

        data = {
            "courseName": "James",
            "preferredTimeSlots": [{"day": "Monday", "startTime": "08:00", "endTime": "10:00"}]
        }

        response = self.client.post(reverse('add_course'), json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn('Course added successfully', response.json()['status'])

    @patch('university_timetabling.timetable.views.timeslots_collection')
    def test_add_time_slot(self, mock_timeslots_collection):
        mock_timeslots_collection.has.return_value = False
        mock_timeslots_collection.insert.return_value = None

        data = {
            "timeSlots": [
                {"day": "Monday", "startTime": "08:00", "endTime": "10:00"},
                {"day": "Wednesday", "startTime": "14:00", "endTime": "16:00"}
            ]
        }

        response = self.client.post(reverse('add_time_slot'), json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn('Time Slot(s) added successfully', response.json()['status'])

    @patch('university_timetabling.timetable.views.instructors_collection')
    @patch('university_timetabling.timetable.views.courses_collection')
    @patch('university_timetabling.timetable.views.timeslots_collection')
    def test_generate_schedule(self, mock_timeslots_collection, mock_courses_collection, mock_instructors_collection):
        mock_instructors_collection.all.return_value = [
            {"name": "James", "preferredCourses": [{"courseName": "Math"}], "availability": [{"day": "Monday", "startTime": "08:00", "endTime": "10:00"}]}
        ]

        mock_courses_collection.all.return_value = [
            {"courseName": "Math", "preferredTimeSlots": [{"day": "Monday", "startTime": "08:00", "endTime": "10:00"}]}
        ]

        mock_timeslots_collection.all.return_value = [
            {"day": "Monday", "startTime": "08:00", "endTime": "10:00"},
            {"day": "Wednesday", "startTime": "14:00", "endTime": "16:00"}
        ]

        response = self.client.post(reverse('schedule'), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn('schedule', response.json())

    @patch('university_timetabling.timetable.views.instructors_collection')
    @patch('university_timetabling.timetable.views.courses_collection')
    @patch('university_timetabling.timetable.views.timeslots_collection')
    def test_generate_schedule(self, mock_timeslots_collection, mock_courses_collection, mock_instructors_collection):
        mock_instructors_collection.all.return_value = [
            {"name": "James", "preferredCourses": [{"courseName": "Math"}], "availability": [{"day": "Monday", "startTime": "08:00", "endTime": "10:00"}]}
        ]

        mock_courses_collection.all.return_value = [
            {"courseName": "Math", "preferredTimeSlots": [{"day": "Tuesday", "startTime": "11:00", "endTime": "13:00"}]},
            {"courseName": "History", "preferredTimeSlots": [{"day": "Monday", "startTime": "10:00", "endTime": "12:00"},
                                                        {"day": "Wednesday", "startTime": "13:00", "endTime": "15:00"}]}

        ]

        mock_timeslots_collection.all.return_value = [
            {"day": "Monday", "startTime": "11:00", "endTime": "14:00"},
            {"day": "Wednesday", "startTime": "14:00", "endTime": "16:00"},
            {"day": "Tuesday", "startTime": "11:00", "endTime": "13:00"}
        ]

        response = self.client.post(reverse('schedule'), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn('schedule', response.json())

    @patch('university_timetabling.timetable.views.db')
    def test_show_university(self, mock_db):
        mock_db.collection.return_value.all.side_effect = [
            [{"courseName": "Math"}],
            [{"name": "James"}],
            [{"day": "Monday", "startTime": "08:00", "endTime": "10:00"}]
        ]

        response = self.client.get(reverse('show_university'))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('courses', data)
        self.assertIn('instructors', data)
        self.assertIn('timeSlots', data)


if __name__ == '__main__':
    unittest.main()