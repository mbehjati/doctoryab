from django.conf.urls import url

from . import views

app_name = 'appointment'
urlpatterns = [
    url(r'^doctor/(?P<doctor_id>[0-9]+)/$', views.doctor_detail, name='detail'),
    url(r'^doctor_times/(?P<doctor_id>[0-9]+)/$', views.get_appointments, name='appointments'),
    url(r'^get-doctor/(?P<doctor_id>[0-9]+)/$', views.get_doctor, name='doci'),
    url(r'^api/reserve/$', views.reserve_appointment, name='reserve_app'),
    url(r'search-key/', views.search_keyword),

]
