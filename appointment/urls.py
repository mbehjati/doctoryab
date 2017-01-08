from django.conf.urls import url

from . import views

app_name = 'appointment'
urlpatterns = [
    url(r'^doctor/(?P<doctor_id>[0-9]+)/$', views.doctor_detail, name='detail'),
]
