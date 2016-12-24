from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.test import TestCase
from .models import MyUser, User, Doctor
from .forms import *
# UserForm, MyUserForm, DoctorForm, L
from .views import register


class UserModelsTest(TestCase):

    def add_new_users(self):
        self.user1 = User.objects.create(username='user1', password='12345', email='m.soleimani73.z@gmail.com')
        self.myuser1 = MyUser.objects.create(user=self.user1, phone_number='09109999999', national_code='1200153374')
        # self.doc1 = Doctor.objects.create(user=self.myuser1, university='tehran', year_diploma='1995', expertise='')

    def test_new_users_activation(self):
        self.add_new_users()
        self.assertEqual(self.user1.is_active, True)
        self.assertEqual(self.myuser1.is_active, True)
        # self.assertEqual(self.doc1.user.is_active, True)

    def test_users_added(self):
        self.add_new_users()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(Doctor.objects.count(), 0)


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

    def test_registration_form_no_empty_user_pass_fields(self):
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


# class UserRegistrationView(TestCase):
#
#     def test_registration_User(self):
#         response = self.client.get('user/register', follow=True)
#         # response = self.client.post(reversed('/user/register'),
#         #                          data={'username': 'user1',
#         #                                'password': '12345',
#         #                                'password2': '12345',
#         #                                'email': 'm.solieimani73.z@gmail.com'
#         #                                })
#         # self.assertEqual(user1.status_code, 200)
#         # self.assertEqual(user1['location'], 200)
#         # last_url, status
#         # _code = response.redirect_chain[-1]
#         print(response.url)
#         # last_url)

class UserLogin(UserModelsTest):

    def test_valid_user_login(self):
        UserModelsTest.add_new_users(self)
        form1 = LoginForm(data={'username': 'user1',
                                'password': '12345'})
        self.assertEqual(form1.is_valid(), True)

    # def test_valid_user_login_view(self):
    #     UserModelsTest.add_new_users(self)
    #     # self.user = authenticate(username='user1', password='12345')
    #     # self.assertTrue(self.user)
    #     self.client.login(username='user1', password='12345')
    #     response = self.client.get('/manufacturers/', follow=True)
    #     user = User.objects.get(username='temporary')
    #     self.assertEqual(response.context['email'], 'temporary@gmail.com')


