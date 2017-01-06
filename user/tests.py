from django.test import TestCase
from .views import *
from django.core.files.uploadedfile import SimpleUploadedFile


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
