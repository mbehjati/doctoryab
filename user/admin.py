from django.contrib import admin

from user.models import MyUser, Doctor, Insurance, Expertise


@admin.register(MyUser)
class AdminMyUser(admin.ModelAdmin):
    pass


@admin.register(Doctor)
class AdminDoctor(admin.ModelAdmin):
    pass


@admin.register(Insurance)
class AdminInsurance(admin.ModelAdmin):
    pass


@admin.register(Expertise)
class AdminExpertise(admin.ModelAdmin):
    pass
