# -*- coding: UTF-8 -*-

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from appointment.serializers import AppointmentSerializer
from user.models import Doctor, MyUser, Insurance, Expertise


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('user', 'diploma', 'office_address', 'office_phone_number', 'expertise', 'insurance', 'title')
        depth = 3


class MyUserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'  # TODO: see what we need and we don't
        depth = 2


class DateAppointmentSerializer(serializers.Serializer):
    date = serializers.CharField(max_length=10)
    appointments = AppointmentSerializer(many=True)


class InsuranceSerializer(ModelSerializer):
    class Meta:
        model = Insurance
        fields = ('name', '')


class ExpertiseSerializer(ModelSerializer):
    class Meta:
        model = Expertise
        fields = ('name',)
