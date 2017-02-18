from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from appointment.models import AppointmentTime


class AppointmentSerializer(ModelSerializer):
    get_status = serializers.ReadOnlyField()

    class Meta:
        model = AppointmentTime
        depth = 3
        fields = '__all__'
