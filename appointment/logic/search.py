# -*- coding: UTF-8 -*-
from appointment.models import AppointmentTime
from user.models import Doctor


def do_advanced_search(form):
    if form.is_valid():
        doctors = search_by_name(Doctor.objects.all(), form.cleaned_data['name'])
        doctors = search_by_expertise(doctors, form.cleaned_data['expertise'])
        doctors = search_by_date(doctors, form.cleaned_data['date'], AppointmentTime.objects.all())
        doctors = search_by_address(doctors, form.cleaned_data['address'])
        doctors = search_by_insurance(doctors, form.cleaned_data['insurance'])
        return doctors


def search_by_name(doctors, name):
    ans = []
    for doc in doctors:
        if name.replace(' ', '') in (doc.user.user.first_name + doc.user.user.last_name).replace(' ', ''):
            ans.append(doc)
    return ans


def search_by_expertise(doctors, expertise):
    if expertise == 'همه':
        return doctors

    return [doc for doc in doctors if doc.expertise.name == expertise]


def search_by_date(doctors, date, app_times):
    if date == '':
        return doctors

    ans = [app_time.doctor for app_time in app_times if app_time.date == date and app_time.doctor]
    return list(set(ans).intersection(set(doctors)))


def search_by_address(doctors, address):
    return [doc for doc in doctors if address in doc.office_address]


def search_by_insurance(doctors, insurance):
    if insurance == 'همه':
        return doctors

    return [doc for doc in doctors for ins in doc.insurance.all() if ins.name == insurance]


def search_by_name_or_expertise(doctors, keyword):
    ans1 = search_by_expertise(doctors, keyword)
    ans2 = search_by_name(doctors, keyword)
    return list(set(ans2).union(set(ans1)))
