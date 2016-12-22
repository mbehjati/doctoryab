from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.doctor_free_time, name='index'),
]
