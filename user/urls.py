from django.conf.urls import url
from user import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^profile', views.view_profile, name='viewProfile'),
    url(r'^editProfile$', views.edit_profile, name='EditProfile'),

]