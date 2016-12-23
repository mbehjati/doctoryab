from django.contrib import admin

from user.models import MyUser , Doctor


@admin.register(MyUser)
class AdminMyUser(admin.ModelAdmin):
    pass


@admin.register(Doctor)
class AdminDoctor(admin.ModelAdmin):
    pass


