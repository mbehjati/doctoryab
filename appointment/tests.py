# Create your tests here.
from django.test import TestCase

from .forms import DoctorFreeTimes


class DoctorFreeTimeFormTest(TestCase):

    def test_is_valid_data(self):
        test = DoctorFreeTimes()

        test.start_time = '12:00am'
        test.end_time = '12:15am'
        test.start_date = '1395-07-09'
        test.end_date = '1395-07-10'
        self.assertEqual(test.is_data_valid(), True)

        test.start_time = '12:30am'
        test.end_time = '12:15pm'
        test.start_date = '1395-07-09'
        test.end_date = '1395-07-10'
        self.assertEqual(test.is_data_valid(), True)

        test.start_time = '1:00pm'
        test.end_time = '5:15am'
        test.start_date = '1395-07-09'
        test.end_date = '1395-07-10'
        self.assertEqual(test.is_data_valid(), False)

        test.start_time = '1:00am'
        test.end_time = '2:15am'
        test.start_date = '1395-07-09'
        test.end_date = '1395-07-10'
        self.assertEqual(test.is_data_valid(), True)

        test.start_time = '1:00pm'
        test.end_time = '12:15pm'
        test.start_date = '1395-07-09'
        test.end_date = '1395-07-10'
        self.assertEqual(test.is_data_valid(), False)

        test.start_time = '12:00am'
        test.end_time = '12:15am'
        test.start_date = '1395-07-11'
        test.end_date = '1395-07-10'
        self.assertEqual(test.is_data_valid(), False)

        test.start_time = '12:00am'
        test.end_time = '12:15am'
        test.start_date = '1395-12-09'
        test.end_date = '1395-08-10'
        self.assertEqual(test.is_data_valid(), False)






