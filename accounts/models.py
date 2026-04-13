from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [('admin', '管理员'), ('student', '考生')]
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES, default='student')
    department = models.CharField('供应商名称', max_length=100, blank=True, default='')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
