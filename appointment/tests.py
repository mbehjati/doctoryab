# Create your tests here.
# -*- coding: UTF-8 -*-
from django.test import TestCase

from appointment.logic.appointment_time import sort_appointment_times_in_day, is_time_before, add_time, \
    sort_appointment_times, cluster_appointment_times
from appointment.logic.doctor_plan import calc_doctor_free_times, has_appointment_conflict, calc_visit_times_for_a_day
from appointment.logic.search import search_by_name, search_by_expertise, search_by_date, search_by_address, \
    search_by_insurance
from user.models import Expertise, Insurance
from .views import *


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


class AddDoctorFreeTime(TestCase):
    user = User(username='doc1', password='12345678')
    myuser = MyUser(user=user, phone_number='09361827280', national_code='1234567890')
    doc1 = Doctor(user=myuser, university='teh', year_diploma='1390', diploma='tajrobi', office_address='addr',
                  office_phone_number='09123456789')

    user = User(username='doc2', password='12345678', first_name='doc2 f', last_name='doc2 l')
    myuser = MyUser(user=user, phone_number='09361827280', national_code='1234567890')
    doc2 = Doctor(user=myuser, university='teh', year_diploma='1390', diploma='tajrobi', office_address='addr teh',
                  office_phone_number='09123456789')

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

    def test_calc_doctor_free_time(self):
        test = DoctorFreeTimes()
        test.start_time = '12:00pm'
        test.end_time = '1:00pm'
        test.start_date = '1395-07-01'
        test.end_date = '1395-07-02'
        test.visit_duration = 30

        app1 = AppointmentTime(start_time='12:00pm', end_time='12:30pm', date='1395-07-01', doctor=self.doc1,
                               duration=30)
        app2 = AppointmentTime(start_time='12:30pm', end_time='1:00pm', date='1395-07-01', doctor=self.doc1,
                               duration=30)
        app3 = AppointmentTime(start_time='12:00pm', end_time='12:30pm', date='1395-07-02', doctor=self.doc1,
                               duration=30)
        app4 = AppointmentTime(start_time='12:30pm', end_time='1:00pm', date='1395-07-02', doctor=self.doc1,
                               duration=30)

        self.assertEqual(calc_doctor_free_times(self.doc1, test), [app1, app2, app3, app4])

        test.start_time = '11:30am'
        test.end_time = '1:15pm'
        app5 = AppointmentTime(start_time='11:30am', end_time='12:00pm', date='1395-07-01', doctor=self.doc1,
                               duration=30)
        app6 = AppointmentTime(start_time='11:30am', end_time='12:00pm', date='1395-07-02', doctor=self.doc1,
                               duration=30)
        self.assertEqual(calc_doctor_free_times(self.doc1, test), [app5, app1, app2, app6, app3, app4])

    def test_calc_visit_times_for_a_day(self):
        app1 = AppointmentTime(start_time='12:00pm', end_time='12:30pm', date='1395-07-01', doctor=self.doc1,
                               duration=30)
        app2 = AppointmentTime(start_time='12:30pm', end_time='13:00pm', date='1395-07-01', doctor=self.doc1,
                               duration=30)
        app5 = AppointmentTime(start_time='11:30am', end_time='12:00pm', date='1395-07-01', doctor=self.doc1,
                               duration=30)
        start_time = '11:30am'
        end_time = '1:15pm'
        duration = 30

        self.assertEqual(calc_visit_times_for_a_day(self.doc1, '1395-07-01', start_time, end_time, duration),
                         [app5, app1, app2])

    def test_has_appointment_conflict(self):
        app = AppointmentTime(start_time='12:00pm', end_time='12:30pm', date='1395-07-01', doctor=self.doc1,
                              duration=30)
        new_app = AppointmentTime(start_time='12:00pm', end_time='12:30pm', date='1395-07-01', doctor=self.doc1,
                                  duration=30)

        self.assertEqual(has_appointment_conflict(new_app, [app]), True)

        new_app.start_time = '12:15pm'
        self.assertEqual(has_appointment_conflict(new_app, [app]), True)

        new_app.end_time = '12:25pm'
        self.assertEqual(has_appointment_conflict(new_app, [app]), True)

        new_app.start_time = '11:30am'
        new_app.end_time = '12:00pm'
        self.assertEqual(has_appointment_conflict(new_app, [app]), False)

        new_app.end_time = '12:01pm'
        self.assertEqual(has_appointment_conflict(new_app, [app]), True)

        new_app.end_time = '13:00pm'
        new_app.start_time = '12:30pm'
        self.assertEqual(has_appointment_conflict(new_app, [app]), False)

        new_app.start_time = '12:00pm'
        new_app.end_time = '12:30pm'
        new_app.date = '1395-07-02'
        self.assertEqual(has_appointment_conflict(new_app, [app]), False)

        new_app.date = '1395-07-01'
        new_app.doctor = self.doc2
        self.assertEqual(has_appointment_conflict(new_app, [app]), False)


class SearchDoctor(TestCase):
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
        exp_ans = [{'date': '1395-07-01', 'apps': [self.app1, self.app2, self.app3, self.app4, self.app8]},
                   {'date': '1395-07-02', 'apps': [self.app6, self.app7]},
                   {'date': '1395-07-03', 'apps': [self.app5]}]
        self.assertEqual(get_doctor_all_plan('1395-07-01', self.doc1), exp_ans)

    def test_cluster_appointment_times(self):
        self.add_objects()
        exp_ans = [{'date': '1395-07-01', 'apps': [self.app1, self.app2, self.app3, self.app4, self.app8]},
                   {'date': '1395-07-02', 'apps': [self.app6, self.app7]},
                   {'date': '1395-07-03', 'apps': [self.app5]}]
        self.assertEqual(cluster_appointment_times(
            [self.app1, self.app2, self.app3, self.app4, self.app8, self.app6, self.app7, self.app5]), exp_ans)
