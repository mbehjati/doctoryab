# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-24 01:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0003_auto_20161224_0121'),
        ('appointment', '0004_auto_20161223_1822'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Expertise',
        ),
        migrations.DeleteModel(
            name='Insurance',
        ),
    ]
