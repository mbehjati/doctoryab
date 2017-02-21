# -*- coding: UTF-8 -*-
from django import forms
from django.db import OperationalError

from user.models import Insurance, Expertise


class DoctorFreeTimes(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    visit_duration = forms.Select()

    def is_data_valid(self):
        if self.start_date == '' or self.end_date == '' or self.start_time == '' or self.end_time == '':
            return False
        if self.start_date > self.end_date:
            return False
        if 'pm' in self.start_time and 'am' in self.end_time:
            return False
        if 'am' in self.start_time and 'pm' in self.end_time:
            return True
        if '12:' in self.start_time and '12:' not in self.end_time:
            return True
        if self.start_time >= self.end_time:
            return False
        return True


class AdvancedSearchForm(forms.Form):
    insurance_choices = (('همه', 'همه'),)
    expertise_choices = (('همه', 'همه'),)
    try:
        for ins in Insurance.objects.all():
            insurance_choices += ((ins.name, ins.name),)

        for exp in Expertise.objects.all():
            expertise_choices += ((exp.name, exp.name),)
    except OperationalError:
        pass

    name = forms.CharField(label='نام پزشک', required=False)
    expertise = forms.ChoiceField(choices=expertise_choices, label='تخصص')
    date = forms.CharField(label='تاریخ', required=False)
    insurance = forms.ChoiceField(choices=insurance_choices, label='بیمه')
    address = forms.CharField(label='آدرس', required=False)
