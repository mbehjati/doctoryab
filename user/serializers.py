# -*- coding: UTF-8 -*-

from rest_framework.serializers import ModelSerializer

from user.models import Doctor, MyUser, Insurance, Expertise


class DoctorSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('user', 'diploma', 'office_address', 'office_phone_number', 'expertise', 'insurance', 'title', 'id')
        depth = 3


class MyUserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'  # TODO: see what we need and we don't
        depth = 2


class InsuranceSerializer(ModelSerializer):
    class Meta:
        model = Insurance
        fields = ('name', '')


class ExpertiseSerializer(ModelSerializer):
    class Meta:
        model = Expertise
        fields = ('name',)
