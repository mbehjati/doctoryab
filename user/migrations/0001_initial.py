# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-09 09:49
from __future__ import unicode_literals

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university', models.CharField(max_length=60)),
                ('year_diploma', models.CharField(blank=True, max_length=4, validators=[
                    django.core.validators.RegexValidator(message='سال وارد شده باید 4 رقمی و با ارقام انگلیسی باشد.',
                                                          regex='([0-9]{4})')])),
                ('diploma', models.CharField(choices=[('عمومی', 'عمومی'), ('تخصص', 'تخصص'), ('فوق تخصص', 'فوق تخصص')],
                                             max_length=12)),
                ('office_address', models.CharField(max_length=300)),
                ('office_phone_number', models.CharField(blank=True, max_length=11, validators=[
                    django.core.validators.RegexValidator(
                        message='شماره تلفن وارد شده باید 11 رقمی بوده و با صفر شروع شود و با ارقام انگلیسی باشد.',
                        regex='^([0]{1})([0-9]{10})$')])),
                ('contract', models.FileField(upload_to='contracts')),
            ],
        ),
        migrations.CreateModel(
            name='Expertise',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=11, validators=[
                    django.core.validators.RegexValidator(
                        message='شماره تلفن وارد شده باید 11 رقمی بوده و با صفر شروع شود و با ارقام انگلیسی باشد.',
                        regex='^([0]{1})([0-9]{10})$')])),
                ('national_code', models.CharField(blank=True, max_length=10, validators=[
                    django.core.validators.RegexValidator(
                        message='کدملی وارد شده باید 10 رقمی و با ارقام انگلیسی باشد.', regex='^([0-9]{10})$')])),
                ('image', models.ImageField(blank=True, upload_to='images')),
                ('is_doctor', models.BooleanField(default=False)),
                (
                'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='expertise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Expertise'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='insurance',
            field=models.ManyToManyField(to='user.Insurance'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(default='1', on_delete=django.db.models.deletion.CASCADE, to='user.MyUser'),
        ),
    ]
