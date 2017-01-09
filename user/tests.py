from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from appointment.models import AppointmentTime
from user.doctor_plan import calc_doctor_free_times, calc_visit_times_for_a_day, has_appointment_conflict
from .views import *


class UserModelsTest(TestCase):
    def add_new_users(self):
        self.user1 = User.objects.create(username='user1', password='12345', email='m.soleimani73.z@gmail.com')
        self.myuser1 = MyUser.objects.create(user=self.user1, phone_number='09109999999', national_code='1200153374')

        self.user2 = User.objects.create_user(username='doc1', password='12345', email='m.soleimani73.z@gmail.com')
        self.myuser2 = MyUser.objects.create(user=self.user2, phone_number='09109999999', national_code='1200153374',
                                             is_doctor='True')
        self.expertise = Expertise.objects.create(name='expert')
        self.doc1 = Doctor.objects.create(user=self.myuser2, university='tehran', year_diploma='1995',
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
        self.assertEqual(self.myuser1.is_active, True)
        self.assertEqual(self.doc1.user.is_active, True)

    def test_users_added(self):
        self.add_new_users()
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(MyUser.objects.count(), 2)
        self.assertEqual(Doctor.objects.count(), 1)
        self.assertEqual(self.user1.password, '12345')
        self.assertEqual(self.myuser1.phone_number, '09109999999')
        self.assertEqual(self.doc1.university, 'tehran')


class UserRegistrationForm(UserModelsTest):
    def test_register_form_passes_similarity(self):
        form1 = UserForm(data={'username': 'user1',
                               'password': '12345',
                               'password2': '12345'})
        self.assertEqual(form1.is_valid(), True)
        form2 = UserForm(data={'username': 'user1',
                               'password': '123456',
                               'password2': '12345'})

        self.assertEqual(form2.is_valid(), False)

    def test_registration_form_mail_validation(self):
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

    def test_user_reg_form_no_empty_fields(self):
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

    def test_myuser_form_validation(self):
        form1 = MyUserForm(data={'phone_number': '09109999999',
                                 'national_code': '1200153374'})
        self.assertEqual(form1.is_valid(), True)

        form2 = MyUserForm(data={'phone_number': '9109999999',
                                 'national_code': '1200153374'})

        self.assertEqual(form2.is_valid(), False)

        form3 = MyUserForm(data={'phone_number': '09109999999',
                                 'national_code': '200153374'})
        self.assertEqual(form3.is_valid(), False)


class UserLogin(UserModelsTest):
    def test_valid_user_login_view(self):
        self.user1 = User.objects.create_user(username='user1', password='12345', email='m.soleimani73.z@gmail.com')
        user = MyUser.objects.create(user=self.user1, phone_number='09109999999', national_code='1200153374')
        user = authenticate(username='user1', password='12345')
        self.assertTrue(self.client.login(username='user1', password='12345'))

        self.user2 = User.objects.create_user(username='doc1', password='12345', email='m.soleimani73.z@gmail.com')
        self.myuser2 = MyUser.objects.create(user=self.user2, phone_number='09109999999', national_code='1200153374',
                                             is_doctor='True')
        self.expertise = Expertise.objects.create(name='expert')
        upload_file = open('user/static/user/contract/contract.pdf', 'rb')
        self.doc1 = Doctor.objects.create(user=self.myuser2, university='tehran', year_diploma='1995',
                                          office_address='tehran',
                                          office_phone_number='02188888888',
                                          expertise=self.expertise,
                                          contract=SimpleUploadedFile(upload_file.name, upload_file.read()))
        self.insurance1 = self.doc1.insurance.create(name='taminEjtemaiee')
        self.insurance2 = self.doc1.insurance.create(name='niroyeMosallah')
        user = authenticate(username='doc1', password='12345')
        print(self.doc1)
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
        self.user1 = User.objects.create_user(username='user1', password='12345', email='m.soleimani73.z@gmail.com')
        user = MyUser.objects.create(user=self.user1, phone_number='09109999999', national_code='1200153374')
        response = self.client.get('/user/edit-profile')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='user1', password='12345')
        response = self.client.get('/user/edit-profile')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, 'user1')
        self.assertEqual(response.context['myuser'].phone_number, '09109999999')

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
        self.user2 = User.objects.create_user(username='doc1', password='12345', email='m.soleimani73.z@gmail.com')
        self.myuser2 = MyUser.objects.create(user=self.user2, phone_number='09109999999', national_code='1200153374',
                                             is_doctor='True')
        self.expertise = Expertise.objects.create(name='expert')
        upload_file = open('user/static/user/contract/contract.pdf', 'rb')
        self.doc1 = Doctor.objects.create(user=self.myuser2, university='tehran', year_diploma='1995',
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
        self.client.login(username='doc1', password='12345')
        response = self.client.get('/user/edit-profile')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, 'doc1')
        self.assertEqual(response.context['myuser'].phone_number, '09109999999')
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
    myuser = MyUser(user=user, phone_number='09361827280', national_code='1234567890')
    doc1 = Doctor(user=myuser, university='teh', year_diploma='1390', diploma='tajrobi', office_address='addr',
                  office_phone_number='09123456789')

    user = User(username='doc2', password='12345678', first_name='doc2 f', last_name='doc2 l')
    myuser = MyUser(user=user, phone_number='09361827280', national_code='1234567890')
    doc2 = Doctor(user=myuser, university='teh', year_diploma='1390', diploma='tajrobi', office_address='addr teh',
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
