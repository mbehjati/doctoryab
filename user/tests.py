from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import RequestFactory

from user.doctor_plan import calc_doctor_free_times, calc_visit_times_for_a_day, has_appointment_conflict
from .forms.doctorplan import DoctorFreeTimes
from .views import *

STATUS_OK = 200


class UserModelsTest(TestCase):
    def add_new_users(self):
        self.user1 = User.objects.create(username='user1', password='12345', email='m.soleimani73.z@gmail.com')
        self.my_user1 = MyUser.objects.create(user=self.user1, phone_number='09109999999', national_code='1200153374')

        self.user2 = User.objects.create_user(username='doc1', password='12345', email='m.soleimani73.z@gmail.com')
        self.my_user2 = MyUser.objects.create(user=self.user2, phone_number='09109999999', national_code='1200153374',
                                              is_doctor='True')
        self.expertise = Expertise.objects.create(name='expert')
        self.doc1 = Doctor.objects.create(user=self.my_user2, university='tehran', year_diploma='1995',
                                          office_address='tehran',
                                          office_phone_number='02188888888',
                                          expertise=self.expertise)
        self.insurance1 = self.doc1.insurance.create(name='taminEjtemaiee')
        self.insurance2 = self.doc1.insurance.create(name='niroyeMosallah')
        upload_file = open('user/static/user/contract/contract.pdf', 'rb')
        self.doc1.contract = SimpleUploadedFile(upload_file.name, upload_file.read())

    def test_new_users_activation(self):
        self.add_new_users()
        self.assertEqual(self.user1.is_active, True)
        self.assertEqual(self.my_user1.is_active, True)
        self.assertEqual(self.doc1.user.is_active, True)

    def test_users_added(self):
        self.add_new_users()
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(MyUser.objects.count(), 2)
        self.assertEqual(Doctor.objects.count(), 1)
        self.assertEqual(self.user1.password, '12345')
        self.assertEqual(self.my_user1.phone_number, '09109999999')
        self.assertEqual(self.doc1.university, 'tehran')


class UserRegistrationForm(UserModelsTest):
    def test_passes_(self):
        """ checks entered password and password confirmation to be similar """
        form1 = UserForm(data={'username': 'user1',
                               'password': '12345',
                               'password2': '12345'})
        self.assertEqual(form1.is_valid(), True)
        form2 = UserForm(data={'username': 'user1',
                               'password': '123456',
                               'password2': '12345'})
        self.assertEqual(form2.is_valid(), False)

    def test_mail_validation(self):
        """ checks entered mail fields in registration form to be valid"""
        form1 = UserForm(data={'username': 'user1',
                               'password': '12345',
                               'password2': '12345',
                               'email': 'm.solieimani73.z@gmail.com'
                               })
        self.assertEqual(form1.is_valid(), True)
        form2 = UserForm(data={'username': 'user1',
                               'password': '12345',
                               'password2': '12345',
                               'email': 'm.solieimani73.z'
                               })
        self.assertEqual(form2.is_valid(), False)

        form3 = UserForm(data={'username': 'user1',
                               'password': '12345',
                               'password2': '12345',
                               'email': 'm.solieimani73.z',
                               'phone_number': '09109999999',
                               'national_code': '1200153374'
                               })
        self.assertEqual(form3.is_valid(), False)

        form4 = UserForm(data={'username': 'user1',
                               'password': '12345',
                               'password2': '12345',
                               'email': 'm.solieimani73.z',
                               'phone_number': '9109999999',
                               'national_code': '1200153374'})
        self.assertEqual(form4.is_valid(), False)

        form5 = UserForm(data={'username': 'user1',
                               'password': '12345',
                               'password2': '12345',
                               'email': 'm.solieimani73.z',
                               'phone_number': '09109999999',
                               'national_code': '200153374'})
        self.assertEqual(form5.is_valid(), False)

    def test_no_empty_fields(self):
        """ checks user registration form required fields to bi filled by user"""
        form1 = UserForm(data={'username': 'user1',
                               'password': '12345',
                               'password2': '12345',
                               })

        self.assertEqual(form1.is_valid(), True)

        form2 = UserForm(data={'password': '12345',
                               'password2': '12345',
                               })
        self.assertEqual(form2.is_valid(), False)

        form3 = UserForm(data={'username': 'user1',
                               'password2': '12345',
                               })
        self.assertEqual(form3.is_valid(), False)

        form4 = UserForm(data={'username': 'user1',
                               'password': '12345',
                               })
        self.assertEqual(form4.is_valid(), False)

    def test_not_duplicate_username(self):
        UserModelsTest.add_new_users(self)
        form1 = UserForm(data={'username': 'user1',
                               'password': '12345',
                               'password2': '12345',
                               'email': 'm.solieimani73.z@gmail.com'
                               })
        self.assertEqual(form1.is_valid(), False)


class UserLogin(TestCase):
    def test_user_login_view(self):
        """checks log in of registered and active users """
        self.user1 = User.objects.create_user(username='user1', password='12345', email='m.soleimani73.z@gmail.com')
        user = MyUser.objects.create(user=self.user1, phone_number='09109999999', national_code='1200153374')
        user = authenticate(username='user1', password='12345')
        self.assertTrue(self.client.login(username='user1', password='12345'))

        self.user2 = User.objects.create_user(username='doc1', password='12345', email='m.soleimani73.z@gmail.com')
        self.my_user2 = MyUser.objects.create(user=self.user2, phone_number='09109999999', national_code='1200153374',
                                              is_doctor='True')
        self.expertise = Expertise.objects.create(name='expert')
        upload_file = open('user/static/user/contract/contract.pdf', 'rb')
        self.doc1 = Doctor.objects.create(user=self.my_user2, university='tehran', year_diploma='1995',
                                          office_address='tehran',
                                          office_phone_number='02188888888',
                                          expertise=self.expertise,
                                          contract=SimpleUploadedFile(upload_file.name, upload_file.read()))
        self.insurance1 = self.doc1.insurance.create(name='taminEjtemaiee')
        self.insurance2 = self.doc1.insurance.create(name='niroyeMosallah')
        user = authenticate(username='doc1', password='12345')
        self.assertTrue(self.client.login(username='doc1', password='12345'))


class UserRegistrationView(TestCase):
    def test_registration_User(self):
        # response = self.client.get('/user/register', follow=True)
        response = self.client.post('/user/register', {'username': 'user1',
                                                       'password': '12345',
                                                       'password2': '123456',
                                                       'email': 'm.solieimani73.z@gmail.com',
                                                       'first_name': 'm',
                                                       'last_name': 's',
                                                       'phone_number': '09109999999',
                                                       'national_code': '1200153374'})
        self.assertEqual(response.status_code, 200)
        # print(response.context['user'])
        # self.assertRedirects(response, '/user/edit-profile')
        # self.assertEqual(user1['location'], 200)
        # last_url, status
        # _code = response.redirect_chain[-1]
        # print(response)
        # last_url)


class UserViewProfileTests(TestCase):
    def test_view_profile(self):
        # first creates user
        self.user1 = User.objects.create_user(username='user1', password='12345', email='m.soleimani73.z@gmail.com')
        user = MyUser.objects.create(user=self.user1, phone_number='09109999999', national_code='1200153374')
        response = self.client.get('/user/edit-profile')
        self.assertEqual(response.status_code, 302)

        # then logs in
        self.client.login(username='user1', password='12345')
        # then edits profile forms
        response = self.client.get('/user/edit-profile')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, 'user1')
        self.assertEqual(response.context['my_user'].phone_number, '09109999999')

        response = self.client.get('/user/edit-profile')
        self.assertEqual(response.context['user'].first_name, '')

        response = self.client.post('/user/edit-profile', {'first_name': 'soli'})
        self.assertRedirects(response, '/user/edit-profile')
        response = self.client.get('/user/edit-profile')
        self.assertEqual(response.context['user'].first_name, 'soli')

        response = self.client.get('/user/edit-password')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/user/edit-password', {'pre_pass': '12345',
                                                            'new_pass': '123456',
                                                            'pass_conf': '123456'})
        self.assertRedirects(response, '/user/edit-profile')


class DoctorViewProfileTests(TestCase):
    def test_view_profile(self):
        """checks doctor register, log in and profile edit as for user"""
        self.user2 = User.objects.create_user(username='doc1', password='12345', email='m.soleimani73.z@gmail.com')
        self.my_user2 = MyUser.objects.create(user=self.user2, phone_number='09109999999', national_code='1200153374',
                                              is_doctor='True')
        self.expertise = Expertise.objects.create(name='expert')
        upload_file = open('user/static/user/contract/contract.pdf', 'rb')
        self.doc1 = Doctor.objects.create(user=self.my_user2, university='tehran', year_diploma='1995',
                                          office_address='tehran',
                                          office_phone_number='02188888888',
                                          expertise=self.expertise,
                                          contract=SimpleUploadedFile(upload_file.name, upload_file.read()))
        self.insurance1 = self.doc1.insurance.create(name='taminEjtemaiee')
        self.insurance2 = self.doc1.insurance.create(name='niroyeMosallah')
        # self.doc1.contract = SimpleUploadedFile('best_file_eva.txt', 'these are the file contents!')

        response = self.client.get('/user/edit-profile')
        self.assertEqual(response.status_code, 302)

        user = authenticate(username='doc1', password='12345')
        # logs registered doctor in
        self.client.login(username='doc1', password='12345')
        response = self.client.get('/user/edit-profile')
        self.assertEqual(response.status_code, 200)
        # changes doctor profile
        self.assertEqual(response.context['user'].username, 'doc1')
        self.assertEqual(response.context['my_user'].phone_number, '09109999999')
        self.assertEqual(response.context['doctor'].office_phone_number, '02188888888')

        response = self.client.get('/user/edit-profile')
        self.assertEqual(response.context['user'].first_name, '')

        response = self.client.post('/user/edit-profile', {'first_name': 'doci',
                                                           'office_address': 'bonab'})
        self.assertRedirects(response, '/user/edit-profile')
        response = self.client.get('/user/edit-profile')
        self.assertEqual(response.context['user'].first_name, 'doci')
        self.assertTrue(MyUser.objects.get(user=user).is_doctor)


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
    my_user = MyUser(user=user, phone_number='09361827280', national_code='1234567890')
    doc1 = Doctor(user=my_user, university='teh', year_diploma='1390', diploma='tajrobi', office_address='addr',
                  office_phone_number='09123456789')

    user = User(username='doc2', password='12345678', first_name='doc2 f', last_name='doc2 l')
    my_user = MyUser(user=user, phone_number='09361827280', national_code='1234567890')
    doc2 = Doctor(user=my_user, university='teh', year_diploma='1390', diploma='tajrobi', office_address='addr teh',
                  office_phone_number='09123456789')

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


class DcotorPlan(TestCase):
    def add_objs(self):
        self.user = User.objects.create(username='doc', password='12345678')
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
                                                   duration=30, patient=self.myuser, confirmation='1')
        self.app3 = AppointmentTime.objects.create(start_time='12:30pm', end_time='13:0pm', date='1395-07-01',
                                                   doctor=self.doc1,
                                                   duration=30, patient=self.myuser, confirmation='1')
        self.app4 = AppointmentTime.objects.create(start_time='12:45pm', end_time='13:15pm', date='1395-07-01',
                                                   doctor=self.doc1,
                                                   duration=30, confirmation='3')

    def test_doctor_free_time_deleted(self):
        self.add_objs()
        self.assertEqual(AppointmentTime.objects.count(), 4)
        rf = RequestFactory()
        request = rf.post('/user/plan', {'app_action': 'delete', 'date': '1395-07-01', 'appointment': self.app1.id,
                                         'cancel_deadline': '1395-07-02'})
        request.user = self.user
        request.session = {}
        response = delete_free_app(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(AppointmentTime.objects.count(), 3)
        self.assertEqual(set(AppointmentTime.objects.all()), set([self.app2, self.app3, self.app4]))

    def test_confirm_appointment(self):
        self.add_objs()
        rf = RequestFactory()
        request = rf.post('/user/plan', {'app_action': 'confirmed', 'date': '1395-07-01', 'appointment': self.app2.id,
                                         'cancel_deadline': '1395-07-02'})
        request.user = self.user
        request.session = {}

        response = app_confirmation(request)
        self.assertEqual(response.status_code, 302)
        self.app2 = AppointmentTime.objects.get(id=self.app2.id)
        self.assertEqual(self.app2.confirmation, '3')

    def test_not_confirm_appointment(self):
        self.add_objs()
        rf = RequestFactory()
        self.assertEqual(AppointmentTime.objects.count(), 4)
        request = rf.post('/user/plan',
                          {'app_action': 'not_confirmed', 'date': '1395-07-01', 'appointment': self.app3.id,
                           'cancel_deadline': '1395-07-02'})
        request.user = self.user
        request.session = {}

        response = app_not_confirmation(request)
        self.assertEqual(response.status_code, 302)
        self.app3 = AppointmentTime.objects.get(id=self.app3.id)
        self.assertEqual(self.app3.confirmation, '2')
        self.assertEqual(AppointmentTime.objects.count(), 5)

    def test_presence_of_appointment(self):
        self.add_objs()
        rf = RequestFactory()
        request = rf.post('user/plan', {'app_action': 'presence', 'date': '1395-07-01', 'appointment': self.app4.id,
                                        'cancel_deadline': '1395-07-02'})
        request.user = self.user
        request.session = {}
        response = set_presence(request)
        self.assertEqual(self.app4.presence, False)
        self.assertEqual(response.status_code, 302)
        self.app4 = AppointmentTime.objects.get(id=self.app4.id)
        self.assertEqual(self.app4.presence, True)

    def test_canceling_of_appointment(self):
        self.add_objs()
        rf = RequestFactory()
        self.assertEqual(AppointmentTime.objects.count(), 4)
        request = rf.post('/user/plan',
                          {'app_action': 'cancel', 'date': '1395-07-01', 'appointment': self.app3.id})
        request.user = self.user
        request.session = {}

        response = cancel_app(request)
        self.assertEqual(response.status_code, 302)
        self.app3 = AppointmentTime.objects.get(id=self.app3.id)
        self.assertEqual(self.app3.confirmation, '2')
        self.assertEqual(AppointmentTime.objects.count(), 5)


class UserViewAppointmentsTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='meli', password='12345678', first_name='melika', last_name='behjati',
                                        email='m@g.com')
        self.patient = MyUser.objects.create(user=user, phone_number='09361827280', national_code='1234567890')

    def test_view_appointments(self):
        self.client.login(username=self.patient.user.username, password='12345678')
        response = self.client.get('/user/appointments')
        self.assertEqual(response.status_code, STATUS_OK)

    def test_login_required(self):
        response = self.client.get('/user/appointments')
        self.assertEqual(response.status_code, 302)


class DoctorWeeklyPlanTest(TestCase):
    def setUp(self):
        # Create Doctor
        user = User.objects.create_user(username='meli', password='12345')
        my_user = MyUser.objects.create(user=user)
        expertise = Expertise.objects.create(name='expert')
        upload_file = open('user/static/user/contract/contract.pdf', 'rb')
        self.doctor = Doctor.objects.create(user=my_user, university='tehran', year_diploma='1995',
                                            office_address='tehran',
                                            office_phone_number='02188888888',
                                            expertise=expertise,
                                            contract=SimpleUploadedFile(upload_file.name, upload_file.read()))
        self.insurance1 = self.doctor.insurance.create(name='taminEjtemaiee')

        # Create Patient
        patient_user = User.objects.create_user(username='mariz', password='12345')
        self.patient = MyUser.objects.create(user=patient_user, phone_number='09194259636')

        # Create Appointments
        today = datetime.now()
        for i in range(7):
            delta = timedelta(i)
            date = today + delta
            formatted_date = jdatetime.date.fromgregorian(date=date).strftime('%Y-%m-%d')
            AppointmentTime.objects.create(patient=self.patient, doctor=self.doctor, date=formatted_date,
                                           end_time='03:00pm',
                                           duration=15, start_time='03:15pm')

    def test_view(self):
        self.client.login(username=self.doctor.user.user.username, password='12345')
        response = self.client.get('/user/weekly-plan')
        self.assertEqual(response.status_code, STATUS_OK)

    def test_get_weekly_plan(self):
        today = datetime.now()
        weekly_plan = get_doctor_weekly_plan(self.doctor, today)
        print(weekly_plan)
        for day_appointments_plan in weekly_plan:
            day_appointments = list(AppointmentTime.objects.filter(doctor=self.doctor, patient=self.patient,
                                                                   date=day_appointments_plan['date']))
            self.assertListEqual(day_appointments_plan['appointments'], day_appointments)

    def test_convert_jalali_gregorian(self):
        jalali_str = '1395-11-16'
        gregorian = convert_jalali_gregorian(jalali_str)
        gregorian_date = date(2017, 2, 4)
        self.assertEqual(gregorian_date, gregorian)
