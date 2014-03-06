from import_export import resources
from django.db import models
from facenew.utils import slug

from djcelery.models import CrontabSchedule

from fandjango.models import User
from djcelery.models import PeriodicTask

from django.db.models.signals import post_save





class Message(models.Model):
	
    def content_file_name(instance, filename):
        return '/'.join(['content', slug(instance.caption), slug(filename)])


    caption = models.CharField('Titulo', max_length=100, blank=False, null= False)
    description = models.CharField('Descripcion', max_length=200, blank=False, null= False)
    message = models.TextField('Mensaje', blank=False, null= False)
    image = models.ImageField(upload_to=content_file_name, blank=True)
    enabled = models.BooleanField('enabled', default=True,)
    date = models.DateField('Fecha de envio', null=False, blank=False)
    link = models.URLField('Link', null=True, blank=True)
    type_message = models.CharField('Tipo de Mensaje', null=False, blank=False, default='facebook', max_length=8, choices=(('facebook', 'Facebook'), ('whatsapp', 'Whatsapp')))
    crontab = models.ForeignKey(
        CrontabSchedule, null=True, blank=False, help_text=('Hora de envio'),
    )

    def __unicode__(self):
        return u'<Message: caption={0}>'.format(self.caption)



class UserCrontabSchedule(models.Model):
    user = models.ForeignKey(User)
    periodic_task = models.ForeignKey(PeriodicTask, null=False)


from facenew.tasks.tasks import assing_new_task
post_save.connect(assing_new_task.delay, sender=Message)