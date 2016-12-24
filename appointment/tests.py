# # Create your tests here.
# from django.test import TestCase
#
# from .views import *
#
#
# class DoctorFreeTimeFormTest(TestCase):
#     def test_is_valid_data(self):
#         test = DoctorFreeTimes()
#
#         test.start_time = '12:00am'
#         test.end_time = '12:15am'
#         test.start_date = '1395-07-09'
#         test.end_date = '1395-07-10'
#         self.assertEqual(test.is_data_valid(), True)
#
#         test.start_time = '12:30am'
#         test.end_time = '12:15pm'
#         test.start_date = '1395-07-09'
#         test.end_date = '1395-07-10'
#         self.assertEqual(test.is_data_valid(), True)
#
#         test.start_time = '1:00pm'
#         test.end_time = '5:15am'
#         test.start_date = '1395-07-09'
#         test.end_date = '1395-07-10'
#         self.assertEqual(test.is_data_valid(), False)
#
#         test.start_time = '1:00am'
#         test.end_time = '2:15am'
#         test.start_date = '1395-07-09'
#         test.end_date = '1395-07-10'
#         self.assertEqual(test.is_data_valid(), True)
#
#         test.start_time = '1:00pm'
#         test.end_time = '12:15pm'
#         test.start_date = '1395-07-09'
#         test.end_date = '1395-07-10'
#         self.assertEqual(test.is_data_valid(), False)
#
#         test.start_time = '12:00am'
#         test.end_time = '12:15am'
#         test.start_date = '1395-07-11'
#         test.end_date = '1395-07-10'
#         self.assertEqual(test.is_data_valid(), False)
#
#         test.start_time = '12:00am'
#         test.end_time = '12:15am'
#         test.start_date = '1395-12-09'
#         test.end_date = '1395-08-10'
#         self.assertEqual(test.is_data_valid(), False)
#
#
# class AddDoctorFreeTime(TestCase):
#     def test_add_time(self):
#         self.assertEqual(add_time('12:15pm', 45), '1:00pm')
#         self.assertEqual(add_time('11:30am', 45), '12:15pm')
#         self.assertEqual(add_time('4:30am', 30), '5:00am')
#         self.assertEqual(add_time('5:15pm', 45), '6:00pm')
#         self.assertEqual(add_time('12:00am', 15), '12:15am')
#
#     def test_is_time_before(self):
#         self.assertEqual(is_time_before('12:45am' , '1:00am') , True)
#         self.assertEqual(is_time_before('12:00pm' , '1:45am') , False)
