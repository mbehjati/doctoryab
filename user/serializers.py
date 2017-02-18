# -*- coding: UTF-8 -*-

from django.db import OperationalError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user.forms.search import AdvancedSearchForm
from user.models import Doctor, MyUser, Insurance, Expertise


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('user', 'diploma', 'office_address', 'office_phone_number', 'expertise', 'insurance')
        depth = 3


class MyUserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'  # TODO: see what we need and we dont
        depth = 2


class SearchFormSerializer(serializers.Serializer):
    insurance_choices = (('همه', 'همه'),)
    expertise_choices = (('همه', 'همه'),)
    try:
        for ins in Insurance.objects.all():
            insurance_choices += ((ins, ins.name),)

        for exp in Expertise.objects.all():
            expertise_choices += ((exp, exp.name),)
    except OperationalError:
        pass
    name = serializers.CharField(label='نام پزشک', required=False)
    expertise = serializers.ChoiceField(choices=expertise_choices, label='تخصص')
    date = serializers.CharField(label='تاریخ', required=False)
    insurance = serializers.ChoiceField(choices=insurance_choices, label='بیمه')
    address = serializers.CharField(label='آدرس', required=False)
