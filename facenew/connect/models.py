from django.db import models

from fandjango.models import User
from djcelery.models import PeriodicTask


class UserCrontabSchedule(models.Model):
    user = models.OneToOneField(User)
    periodic_task = models.ManyToManyField(PeriodicTask, verbose_name='periodic_task', blank=True)