# -*- coding: UTF-8 -*-
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from appointment.logic.appointment_time import sort_appointment_times_in_day, sort_appointment_times, \
    cluster_appointment_times, add_time, is_time_before
from appointment.logic.doctor_plan import get_doctor_day_plan
from appointment.logic.search import search_by_name, search_by_expertise, search_by_date, search_by_address, \
    search_by_insurance
from user.models import Expertise, Insurance
from .views import *


class AppointmentTimeTest(TestCase):
    def test_add_time(self):
        self.assertEqual(add_time('12:15pm', 45), '1:00pm')
        self.assertEqual(add_time('11:30am', 45), '12:15pm')
        self.assertEqual(add_time('4:30am', 30), '5:00am')
        self.assertEqual(add_time('5:15pm', 45), '6:00pm')
        self.assertEqual(add_time('12:00am', 15), '12:15am')
        self.assertEqual(add_time('12:00pm', 30), '12:30pm')

    def test_is_time_before(self):
        self.assertEqual(is_time_before('12:45am', '1:00am'), True)
        self.assertEqual(is_time_before('12:00pm', '1:45am'), False)
        self.assertEqual(is_time_before('12:00pm', '12:00pm'), True)
        self.assertEqual(is_time_before('9:00am', '11:00am'), True)
        self.assertEqual(is_time_before('12:00am', '1:00am'), True)
        self.assertEqual(is_time_before('12:15am', '4:00am'), True)
        self.assertEqual(is_time_before('12:45am', '1:45am'), True)


class SearchDoctorTest(TestCase):
    def add_objs_to_db(self):
        self.exp1 = Expertise.objects.create(name='exp1')
        self.exp2 = Expertise.objects.create(name='exp2')

        self.user = User.objects.create(username='test_doc1', password='12345678', first_name='doc1 f',
                                        last_name='doc1 l')
        self.myuser = MyUser.objects.create(user=self.user, phone_number='09361827280', national_code='1234567890')
        self.doc1 = Doctor.objects.create(user=self.myuser, university='teh', year_diploma='1390', diploma='tajrobi',
                                          office_address='addr',
                                          office_phone_number='09123456789', expertise=self.exp1)

        self.user = User.objects.create(username='test_doc2', password='12345678', first_name='doc2 f exp1',
                                        last_name='doc2 l')
        self.myuser = MyUser.objects.create(user=self.user, phone_number='09361827280', national_code='1234567890')
        self.doc2 = Doctor.objects.create(user=self.myuser, university='teh', year_diploma='1390', diploma='tajrobi',
                                          office_address='addr teh',
                                          office_phone_number='09123456789', expertise=self.exp2)

        self.user = User.objects.create(username='test_doc3', password='12345678', first_name='doc3 f',
                                        last_name='doc3 l')
        self.myuser = MyUser.objects.create(user=self.user, phone_number='09361827280', national_code='1234567890')
        self.doc3 = Doctor.objects.create(user=self.myuser, university='teh', year_diploma='1390', diploma='tajrobi',
                                          office_address='addr2',
                                          office_phone_number='09123456789', expertise=self.exp1)

        self.app1 = AppointmentTime.objects.create(start_time='12:00pm', end_time='12:30pm', date='1395-07-01',
                                                   doctor=self.doc1, duration=30)
        self.app2 = AppointmentTime.objects.create(start_time='12:00pm', end_time='12:30pm', date='1395-07-01',
                                                   doctor=self.doc2, duration=30)
        self.app3 = AppointmentTime.objects.create(start_time='12:00pm', end_time='12:30pm', date='1395-07-02',
                                                   doctor=self.doc1, duration=30)

        self.ins1 = Insurance.objects.create(name='ins1')
        self.ins2 = Insurance.objects.create(name='ins2')

        self.doc1.insurance.add(self.ins1)
        self.doc2.insurance.add(self.ins2)
        self.doc3.insurance.add(self.ins1, self.ins2)

    def test_search_by_name(self):
        self.add_objs_to_db()
        self.assertEqual(search_by_name([self.doc1, self.doc2, self.doc3], 'doc'), [self.doc1, self.doc2, self.doc3])
        self.assertEqual(search_by_name([self.doc1, self.doc2, self.doc3], 'doc1'), [self.doc1])
        self.assertEqual(search_by_name([self.doc1, self.doc2, self.doc3], 'doc4'), [])

    def test_search_by_address(self):
        self.add_objs_to_db()
        self.assertEqual(search_by_address([self.doc1, self.doc2, self.doc3], 'teh'), [self.doc2])
        self.assertEqual(search_by_address([self.doc1, self.doc2, self.doc3], 'addr'),
                         [self.doc1, self.doc2, self.doc3])
        self.assertEqual(search_by_address([self.doc1, self.doc2, self.doc3], 'doc'), [])

    def test_search_by_date(self):
        self.add_objs_to_db()
        self.assertEqual(
            search_by_date([self.doc1, self.doc2, self.doc3], '1395-07-01', [self.app1, self.app2, self.app3]),
            [self.doc1, self.doc2])
        self.assertEqual(
            search_by_date([self.doc1, self.doc2, self.doc3], '1395-07-02', [self.app1, self.app2, self.app3]),
            [self.doc1])

    def test_search_by_expertise(self):
        self.add_objs_to_db()
        self.assertEqual(search_by_expertise([self.doc1, self.doc2, self.doc3], 'exp1'), [self.doc1, self.doc3])
        self.assertEqual(search_by_expertise([self.doc1, self.doc2, self.doc3], 'exp3'), [])
        self.assertEqual(search_by_expertise([self.doc1, self.doc2, self.doc3], 'همه'),
                         [self.doc1, self.doc2, self.doc3])
        self.assertEqual(search_by_expertise([self.doc1, self.doc2], 'exp1'), [self.doc1])

    def test_search_by_insurance(self):
        self.add_objs_to_db()
        self.assertEqual(search_by_insurance([self.doc1, self.doc2, self.doc3], 'ins1'), [self.doc1, self.doc3])
        self.assertEqual(search_by_insurance([self.doc1, self.doc2, self.doc3], 'همه'),
                         [self.doc1, self.doc2, self.doc3])

    def test_search_by_expertise_or_name(self):
        self.add_objs_to_db()
        self.assertEqual(set(search_by_name_or_expertise([self.doc1, self.doc2, self.doc3], "exp1")),
                         set([self.doc1, self.doc2, self.doc3]))
        self.assertEqual(set(search_by_name_or_expertise([self.doc1, self.doc2, self.doc3], "exp2")), set([self.doc2]))
        self.assertEqual(set(search_by_name_or_expertise([self.doc1, self.doc2, self.doc3], "exp")), set([self.doc2]))


class DoctorPlan(TestCase):
    def add_objects(self):
        self.user = User.objects.create(username='t doc1', password='12345678')
        self.myuser = MyUser.objects.create(user=self.user, phone_number='09361827280', national_code='1234567890')
        self.exp1 = Expertise.objects.create(name='exp1')
        self.doc1 = Doctor.objects.create(user=self.myuser, university='teh', year_diploma='1390', diploma='tajrobi',
                                          office_address='addr',
                                          office_phone_number='09123456789', expertise=self.exp1)

        self.app1 = AppointmentTime.objects.create(start_time='12:00pm', end_time='12:30pm', date='1395-07-01',
                                                   doctor=self.doc1,
                                                   duration=30)
        self.app2 = AppointmentTime.objects.create(start_time='12:15pm', end_time='12:345pm', date='1395-07-01',
                                                   doctor=self.doc1,
                                                   duration=30)
        self.app3 = AppointmentTime.objects.create(start_time='12:30pm', end_time='13:0pm', date='1395-07-01',
                                                   doctor=self.doc1,
                                                   duration=30)
        self.app4 = AppointmentTime.objects.create(start_time='12:45pm', end_time='13:15pm', date='1395-07-01',
                                                   doctor=self.doc1,
                                                   duration=30)
        self.app5 = AppointmentTime.objects.create(start_time='12:00pm', end_time='12:30pm', date='1395-07-03',
                                                   doctor=self.doc1,
                                                   duration=30)

        self.app6 = AppointmentTime.objects.create(start_time='12:15pm', end_time='12:345pm', date='1395-07-02',
                                                   doctor=self.doc1,
                                                   duration=30)
        self.app7 = AppointmentTime.objects.create(start_time='12:30pm', end_time='13:0pm', date='1395-07-02',
                                                   doctor=self.doc1,
                                                   duration=30)
        self.app8 = AppointmentTime.objects.create(start_time='13:45pm', end_time='13:15pm', date='1395-07-01',
                                                   doctor=self.doc1,
                                                   duration=30)
        self.app9 = AppointmentTime.objects.create(start_time='1:45pm', end_time='13:15pm', date='1395-07-04',
                                                   doctor=self.doc1,
                                                   duration=30)

    def test_sort_appointment_times_in_day(self):
        self.add_objects()
        self.assertEqual(sort_appointment_times_in_day([self.app3, self.app1, self.app4, self.app2]),
                         [self.app1, self.app2, self.app3, self.app4])
        self.assertEqual(sort_appointment_times_in_day([self.app4, self.app3, self.app2, self.app1]),
                         [self.app1, self.app2, self.app3, self.app4])
        self.assertEqual(sort_appointment_times_in_day([self.app3, self.app1, self.app2, self.app4]),
                         [self.app1, self.app2, self.app3, self.app4])
        self.assertEqual(sort_appointment_times_in_day([self.app2, self.app1, self.app4, self.app3]),
                         [self.app1, self.app2, self.app3, self.app4])
        self.assertEqual(sort_appointment_times_in_day([self.app1, self.app3, self.app4, self.app2]),
                         [self.app1, self.app2, self.app3, self.app4])

        self.assertEqual(sort_appointment_times_in_day([self.app1, self.app9, self.app4, self.app2, self.app3]),
                         [self.app1, self.app2, self.app3, self.app4, self.app9])

    def test_sort_appointment_times(self):
        self.add_objects()
        self.assertEqual(sort_appointment_times(
            [self.app3, self.app1, self.app4, self.app2, self.app7, self.app5, self.app8, self.app6]),
            [self.app1, self.app2, self.app3, self.app4, self.app8, self.app6, self.app7, self.app5])

    def test_get_doctor_day_plan(self):
        self.add_objects()
        self.assertEqual(get_doctor_day_plan('1395-07-01', self.doc1),
                         [self.app1, self.app2, self.app3, self.app4, self.app8])
        self.assertEqual(get_doctor_day_plan('1395-07-02', self.doc1), [self.app6, self.app7])

    def test_get_doctor_plan_all(self):
        self.add_objects()
        exp_ans = [{'date': '1395-07-01', 'appointments': [self.app1, self.app2, self.app3, self.app4, self.app8]},
                   {'date': '1395-07-02', 'appointments': [self.app6, self.app7]},
                   {'date': '1395-07-03', 'appointments': [self.app5]},
                   {'date': '1395-07-04', 'appointments': [self.app9]}]
        self.assertEqual(get_doctor_all_plan('1395-07-01', self.doc1), exp_ans)

    def test_cluster_appointment_times(self):
        self.add_objects()
        exp_ans = [{'date': '1395-07-01', 'appointments': [self.app1, self.app2, self.app3, self.app4, self.app8]},
                   {'date': '1395-07-02', 'appointments': [self.app6, self.app7]},
                   {'date': '1395-07-03', 'appointments': [self.app5]}]
        self.assertEqual(cluster_appointment_times(
            [self.app1, self.app2, self.app3, self.app4, self.app8, self.app6, self.app7, self.app5]), exp_ans)


class APITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_search_keyword(self):
        request = self.factory.post('/search-key/', {'keyword': 'ali'})
        response = search_keyword(request)
        self.assertEqual(response.status_code, 200)