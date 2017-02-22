from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from appointment.models import AppointmentTime


class AppointmentSerializer(ModelSerializer):
    get_status = serializers.ReadOnlyField()

    class Meta:
        model = AppointmentTime
        depth = 3
        fields = '__all__'


class DateAppointmentSerializer(serializers.Serializer):
    date = serializers.CharField(max_length=10)
    appointments = AppointmentSerializer(many=True)
