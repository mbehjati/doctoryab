# -*- coding: UTF-8 -*-
from django import forms
from django.db import OperationalError

from user.models import Insurance, Expertise


class AdvancedSearchForm(forms.Form):
    insurance_choices = (('همه', 'همه'),)
    expertise_choices = (('همه', 'همه'),)
    try:
        for ins in Insurance.objects.all():
            insurance_choices += ((ins, ins.name),)

        for exp in Expertise.objects.all():
            expertise_choices += ((exp, exp.name),)
    except OperationalError:
        pass

    name = forms.CharField(label='نام پزشک', required=False)
    expertise = forms.ChoiceField(choices=expertise_choices, label='تخصص')
    date = forms.CharField(label='تاریخ', required=False)
    insurance = forms.ChoiceField(choices=insurance_choices, label='بیمه')
    address = forms.CharField(label='آدرس', required=False)
