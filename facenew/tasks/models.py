from import_export import resources
from django.db import models
from facenew.utils import slug

class Message(models.Model):
	

    def content_file_name(instance, filename):
        return '/'.join(['content', slug(instance.caption), slug(filename)])


    caption = models.CharField('Titulo', max_length=100, blank=False, null= False)
    description = models.CharField('Descripcion', max_length=200, blank=False, null= False)
    message = models.TextField('Mensaje', blank=False, null= False)
    image = models.ImageField(upload_to=content_file_name)
    enabled = models.BooleanField('enabled', default=True,)


