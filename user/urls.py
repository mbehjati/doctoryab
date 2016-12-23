from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^profile', views.view_profile, name='viewProfile'),
    url(r'^edit-profile$', views.edit_profile, name='EditProfile'),

]