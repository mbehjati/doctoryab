# Register your models here.
from django.contrib import admin

from .models import *


@admin.register(AppointmentTime)
class AdminAppointmentTime(admin.ModelAdmin):
    pass




