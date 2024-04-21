from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20,
                                help_text='昵称',
                                verbose_name='昵称',
                                default='',
                                blank=True)

    telephone = models.CharField(max_length=11,
                                 help_text='手机号码',
                                 verbose_name='手机号码',
                                 default='',
                                 blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
