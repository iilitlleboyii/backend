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
    roles = models.ManyToManyField('Role',
                                   help_text='角色',
                                   verbose_name='角色',
                                   blank=True)

    # department = models.ForeignKey('Department',
    #                                on_delete=models.SET_NULL,
    #                                null=True,
    #                                blank=True,
    #                                help_text='部门',
    #                                verbose_name='部门')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Role(models.Model):
    name = models.CharField(max_length=20,
                            help_text='角色名称',
                            verbose_name='角色名称')
    code = models.CharField(max_length=100,
                            help_text='角色编码',
                            verbose_name='角色编码')
    order = models.IntegerField(default=0, help_text='排序', verbose_name='排序')
    is_active = models.BooleanField(default=True,
                                    help_text='激活',
                                    verbose_name='激活')
    menu_list = models.TextField(help_text='菜单列表',
                                 verbose_name='菜单列表',
                                 default='',
                                 blank=True)
    department_list = models.TextField(help_text='部门列表',
                                       verbose_name='部门列表',
                                       default='',
                                       blank=True)
    description = models.CharField(max_length=150,
                                   help_text='角色描述',
                                   verbose_name='角色描述',
                                   default='',
                                   blank=True)
    created_time = models.DateTimeField(auto_now_add=True,
                                        help_text='创建时间',
                                        verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True,
                                        help_text='更新时间',
                                        verbose_name='更新时间')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name}:{self.code}'
