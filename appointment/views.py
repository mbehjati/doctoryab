# Create your views here.
from django.shortcuts import render

from .forms import DoctorFreeTimes


def index(request):
    return render(request, 'appointment/set_doctor_free_times.html')


def save_doctor_free_times(form):
    pass


def doctor_free_time(request):
    message = ''
    response = False
    if request.method == 'POST':
        form = DoctorFreeTimes()
        form.start_date = request.POST['start_date']
        form.end_date = request.POST['end_date']
        form.start_time = request.POST['start_time']
        form.end_time = request.POST['end_time']
        form.visit_duration = request.POST['visit_duration']
        if form.is_data_valid():
            save_doctor_free_times(form)
            message = 'اطلاعات شما با موفقیت ثبت شد. '
            response = True
        else:
            message = '*اطلاعات واردشده مجاز نمی‌باشد. '

    return render(request, 'appointment/set_doctor_free_times.html', {'message': message, 'response': response})
