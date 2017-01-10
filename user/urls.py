from django.conf.urls import url

from user import views

app_name = 'user'
urlpatterns = [
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^profile', views.view_profile, name='viewProfile'),
    url(r'^edit-profile$', views.edit_profile, name='EditProfile'),
    url(r'^edit-password$', views.edit_password, name='EditPassword'),
    url(r'^enter-plan$', views.doctor_free_time, name='EnterPlan'),
    url(r'^plan$', views.doctor_plan, name='EnterPlan'),
    url(r'^static/user/contract/contract.pdf$', views.upload_contract_file),
]