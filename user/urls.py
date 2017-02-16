from django.conf.urls import url

import user.views
from user import views

app_name = 'user'
urlpatterns = [
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^edit-profile$', views.edit_profile, name='EditProfile'),
    url(r'^edit-password$', views.edit_password, name='EditPassword'),
    url(r'^enter-plan$', views.doctor_free_time, name='EnterPlan'),
    url(r'^plan$', views.doctor_plan, name='EnterPlan'),
    url(r'^static/user/contract/contract.pdf$', views.upload_contract_file),
    url(r'^appointments', views.user_appointments, name='view_appointments'),
    url(r'^weekly-plan', views.doctor_weekly_plan, name='weekly_plan'),
    url(r'^app_confirmation', user.views.app_confirmation, name='app_confirmation'),
    url(r'^app_not_confirmation', user.views.app_not_confirmation, name='app_not_confirmation'),
    url(r'^delete_free_app', user.views.delete_free_app, name='delete_free_app'),
    url(r'^send_presence_mail', user.views.send_presence_mail, name='send_presence_mail'),
    url(r'^cancel_app', user.views.cancel_app, name='cancel_app'),
    url(r'^set_presence', user.views.set_presence, name='set_presence'),

]
