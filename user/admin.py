from django.contrib import admin

from user.models import Doctor, MyUser

admin.site.register(MyUser)
admin.site.register(Doctor)
