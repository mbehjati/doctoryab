from django.contrib.auth.models import User
from django.db import models


class MyUser(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=11)
    # PhoneNumberField()
    national_code = models.IntegerField()
    # validators=[MaxLengthValidator(10),
    #                                                            MinLengthValidator(10)])
    # models.CharField(max_length=11)
    is_active = True

    # address = models.TextField(default="")
    # USERNAME_FIELD = 'username'
    # i=user.id
    # address = models.TextField()

    def __str__(self):
        return self.user.username
