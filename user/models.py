# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Insurance(models.Model):
    name = models.TextField(primary_key=True)

    def __str__(self):
        return self.name


class Expertise(models.Model):
    name = models.TextField(primary_key=True)

    def __str__(self):
        return self.name


class MyUser(models.Model):
    user = models.OneToOneField(User)
    phone_regex = RegexValidator(regex=r'^([0]{1})([0-9]{10})$',
                                 # r'^\+?1?\d{9,15}$',
                                 message="شماره تلفن وارد شده باید 11 رقمی بوده و با صفر شروع شود و با ارقام انگلیسی باشد.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=11)
    national_code_regex = RegexValidator(regex=r'^([0-9]{10})$',
                                         message="کدملی وارد شده باید 10 رقمی و با ارقام انگلیسی باشد.")
    national_code = models.CharField(validators=[national_code_regex], blank=True, max_length=10)
    image = models.ImageField(upload_to='images', blank=True)

    is_active = True
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    user = models.OneToOneField(MyUser, default='1')
    university = models.CharField(max_length=60)
    year_diploma_regex = RegexValidator(regex=r'([0-9]{4})',
                                        message="سال وارد شده باید 4 رقمی و با ارقام انگلیسی باشد.")
    year_diploma = models.CharField(validators=[year_diploma_regex], blank=True, max_length=4)
    diploma = models.CharField(max_length=50)
    office_address = models.CharField(max_length=300)
    phone_regex = RegexValidator(regex=r'^([0]{1})([0-9]{10})$',
                                 message="شماره تلفن وارد شده باید 11 رقمی بوده و با صفر شروع شود و با ارقام انگلیسی باشد.")
    office_phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=11)
    insurance = models.ManyToManyField(Insurance)
    expertise = models.ForeignKey(Expertise)

    contract = models.FileField(upload_to='contracts')

    def __str__(self):
        return str(self.user.user.username)
